# [H-01] Broken implied-price arithmetic corrupts swaps and liquidity valuation

## Affected code

- `src/multi/Edge.sol`: `calcLowerImplied`, `calcUpperImplied`, and
  `calcInnerImplied`

## Root cause

The implied-price routines intend to calculate a reserve ratio at 128-bit
precision and then shift it to 192-bit precision. Instead, their parentheses
place the division inside the shift count. For ordinary reserve values,
`128 / y` or `128 / x` truncates to zero, so the code shifts the numerator by
only 64 bits and never divides by the other reserve.

The inner-range calculation uses the same broken expression. These values feed
the square-root-price and wide-liquidity calculations that the edge uses for
quotes and accounting.

## Prerequisites

- A configured edge processes a swap or liquidity operation.
- Its reserve values are large enough that integer division in the shift count
  truncates, which is the normal operating case.

## Failure sequence

1. The edge selects the lower, upper, or inner implied-price calculation.
2. The reserve-ratio expression is evaluated as a small shift count rather
   than as `(reserve << 128) / otherReserve`.
3. The routine derives an unrelated square-root price and wide liquidity.
4. Swap output and liquidity valuation use the corrupted price state.
5. A trader or liquidity provider receives a materially incorrect asset
   amount, transferring value to the counterparty or pool.

## Impact

The pool can quote and settle swaps or liquidity at a price unrelated to its
actual reserve ratio. Depending on direction, users or the pool lose tokens
through overpayment, underpayment, or incorrect share valuation.

## Code evidence

The lower-range path contains:

```solidity
uint256 xyX192 = (x << (128 / y)) << 64;
```

The upper and inner paths repeat the error with `y` and `x`:

```solidity
uint256 yxX192 = (y << (128 / x)) << 64;
```

## Remediation

Perform the fixed-point division explicitly, such as
`((x << 128) / y) << 64` and `((y << 128) / x) << 64`, and verify every
implied-price branch against a high-precision reference implementation.

# [H-02] Liquidity additions include the deposit in pool value and under-mint shares

## Affected code

- `src/multi/facets/LiqFacet.sol`: `addLiq`
- `src/multi/Asset.sol`: share issuance through `AssetLib.add`

## Root cause

`addLiq` measures the user's newly added balance correctly, but initializes
`cumulativeValue` with the post-deposit token balance. It then prices the
other pre-existing closure balances and passes this inflated denominator to
`AssetLib.add`.

The new deposit is therefore counted in both the share-issuance numerator and
the pool-value denominator. New shares are minted as though the deposit were
already owned by existing LPs.

## Prerequisites

- The closure already has issued shares and pre-existing liquidity.
- A user adds one of the closure's tokens through `LiqFacet.addLiq`.

## Failure sequence

1. The vault balance is read before the deposit.
2. The user's tokens are deposited and the post-deposit `tokenBalance` is
   read.
3. `addedBalance` is computed as the correct balance delta.
4. `cumulativeValue` is incorrectly initialized to the post-deposit balance,
   not `preBalance[idx]`.
5. `AssetLib.add` divides the new contribution by an inflated existing-pool
   value and mints too few shares.
6. Existing LPs capture the omitted ownership value when liquidity is later
   removed.

## Impact

The depositor receives fewer LP shares than the assets contributed justify.
Part of the deposit is irreversibly transferred to existing share holders.

## Code evidence

The balance delta and denominator use inconsistent snapshots:

```solidity
uint256 addedBalance = tokenBalance - preBalance[idx];
uint256 cumulativeValue = tokenBalance;
// ... add the value of every other pre-existing token balance
shares = AssetLib.add(recipient, cid, addedBalance, cumulativeValue);
```

## Remediation

Initialize `cumulativeValue` with `preBalance[idx]`, then add only the value of
the other pre-deposit balances. Test that adding and immediately removing
liquidity returns the contributed pro-rata value, subject only to documented
rounding.

# [H-03] Unrestricted diamond cuts let any caller replace protocol logic

## Affected code

- `src/multi/Diamond.sol`: installation of
  `DiamondCutFacet.diamondCut.selector`
- `lib/Commons/src/Diamond/facets/DiamondCutFacet.sol`: `diamondCut`

## Root cause

`SimplexDiamond` exposes the shared `DiamondCutFacet.diamondCut` entry point,
but that facet performs no owner or admin validation. The intended
`AdminLib.validateLevel(3)` call is commented out.

A diamond cut can add, replace, or remove arbitrary selectors and can also
delegatecall an attacker-selected initialization contract in the diamond's
storage context.

## Prerequisites

- A `SimplexDiamond` instance holds or controls user liquidity.
- Any unprivileged address can submit a transaction to it.

## Exploit sequence

1. The attacker deploys a facet or initialization contract that transfers
   vault assets or rewrites ownership and accounting storage.
2. The attacker calls the diamond's exposed `diamondCut` selector.
3. The unrestricted facet installs the malicious selector or delegatecalls
   the initialization payload.
4. The malicious logic executes in the diamond's storage context.
5. The attacker transfers protocol-controlled tokens or permanently replaces
   the legitimate withdrawal and swap logic.

## Impact

Any caller can take full control of the upgradeable protocol surface and steal
all assets controlled by the diamond or its vault accounting.

## Code evidence

The constructor installs the cut selector:

```solidity
cutFunctionSelectors[0] = DiamondCutFacet.diamondCut.selector;
```

The installed facet omits authorization:

```solidity
function diamondCut(...) external override {
    // todo
    // AdminLib.validateLevel(3);
    LibDiamond.diamondCut(_diamondCut, _init, _calldata);
}
```

## Remediation

Require the appropriate owner or admin level before every diamond cut. Add a
negative test proving that an unprivileged caller cannot add, replace, remove,
or initialize facets.

# [H-04] Unrestricted mint callback spends arbitrary users' token approvals

## Affected code

- `src/Burve.sol`: `uniswapV3MintCallback`

## Root cause

The external mint callback never authenticates `msg.sender` as the configured
Uniswap V3 pool. It also trusts caller-supplied bytes as the token owner and
caller-supplied amounts as the debts to transfer.

Because users approve the Burve contract as spender during normal liquidity
operations, any address can reuse a remaining approval to force tokens from a
victim into the pool without minting the victim a position.

## Prerequisites

- A victim has approved the Burve contract to spend `token0` or `token1`.
- The allowance and balance are still positive.

## Exploit sequence

1. The attacker identifies an address with a live Burve allowance.
2. The attacker calls `uniswapV3MintCallback` directly.
3. The attacker encodes the victim as `source` and supplies amounts within the
   victim's allowances and balances.
4. Burve calls `safeTransferFrom` as the approved spender.
5. The victim's tokens move to the configured pool, but no mint operation
   credits the victim or otherwise compensates the transfer.

## Impact

An arbitrary caller can drain every approved amount from Burve users into the
pool. The victim loses the tokens and receives no LP shares or position.

## Code evidence

The callback is public and performs both transfers without a caller check:

```solidity
function uniswapV3MintCallback(
    uint256 amount0Owed,
    uint256 amount1Owed,
    bytes calldata data
) external {
    address source = abi.decode(data, (address));
    TransferHelper.safeTransferFrom(token0, source, address(pool), amount0Owed);
    TransferHelper.safeTransferFrom(token1, source, address(pool), amount1Owed);
}
```

## Remediation

Require `msg.sender == address(pool)` before decoding callback data or moving
tokens. Keep the payer bound to the active mint call and test direct-callback
attempts from arbitrary addresses.

# [H-05] Mint and burn lack price bounds and expose users to adverse execution

## Affected code

- `src/Burve.sol`: `mint`, `burn`, `mintRange`, `burnRange`, and
  `islandLiqToShares`

## Root cause

The public mint and burn interfaces accept only liquidity and recipient
parameters. They provide no minimum-share, minimum-token, maximum-token, or
price bounds. Island conversions use the pool's current `slot0` price at
execution time, and Uniswap range operations likewise settle at the current
pool state.

A user therefore cannot make the transaction revert when the execution price
moves materially between submission and inclusion.

## Prerequisites

- A user submits a Burve mint or burn transaction.
- Pool price moves naturally or is moved adversarially before that transaction
  executes.

## Adverse-execution sequence

1. The user calculates an acceptable mint or redemption at the observed pool
   price.
2. A searcher moves `slot0` before the user's transaction, or market price
   changes while the transaction is pending.
3. `islandLiqToShares` and the range operations use the new price.
4. The transaction succeeds because the user supplied no enforceable output
   or price bound.
5. The user receives fewer shares or fewer underlying tokens than intended;
   the adverse price mover or existing pool participants capture the value.

## Impact

Users can suffer an unbounded shortfall in shares or redeemed assets while the
transaction still succeeds. This creates a direct sandwich and stale-quote
loss path.

## Code evidence

The entry points contain no slippage parameters:

```solidity
function mint(address recipient, uint128 liq) external { ... }
function burn(uint128 liq) external { ... }
```

The island conversion reads the execution-time pool price:

```solidity
(uint160 sqrtRatioX96,,,,,,) = pool.slot0();
```

## Remediation

Add caller-supplied bounds and a deadline to mint and burn. Enforce minimum
shares or token outputs and maximum token inputs across every configured
range, reverting the entire operation when any bound is violated.
