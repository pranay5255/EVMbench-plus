# VII Finance detect gold audit

## [H-01] Uniswap V4 partial unwraps leave fee credits reusable for repeated theft

### Affected code

- `src/uniswap/UniswapV4Wrapper.sol`: `_unwrap`, `_accumulateFees`, and `tokensOwed`
- `src/ERC721WrapperBase.sol`: the partial and full `unwrap` overloads

### Root cause

`UniswapV4Wrapper._unwrap` adds all newly pending LP fees to the persistent
`tokensOwed[tokenId]` balance and transfers the caller's proportional share,
but it never subtracts the paid share from that balance. The accounting credit
therefore survives after payment and even after the position's ERC-6909 supply
is burned and its underlying NFT is retrieved.

### Prerequisites and exploit sequence

1. A wrapped Uniswap V4 position accrues fees and is partially unwrapped.
2. `_pendingFees` and `_accumulateFees` increase the stored fee credit.
3. `_unwrap` transfers a proportional fee share without consuming the credit.
4. The attacker fully unwraps, increases liquidity, and re-wraps the same NFT,
   receiving a fresh full ERC-6909 supply while the stale credit persists.
5. Another partial unwrap pays against the stale credit and drains tokens that
   back fees owed to other holders.

### Impact

The attacker steals LP-fee assets belonging to other ERC-6909 holders. After
the wrapper's real currency balance is depleted, legitimate unwraps can also
revert and obstruct collateral recovery during liquidation.

### Code evidence and remediation

At audited commit `2a3a72c675a580dcdeb2f7d733d40c6bfb1b3dc7`,
`UniswapV4Wrapper.sol:100-101` accumulates pending fees and lines 108-109
transfer proportional shares directly from `tokensOwed`; no write reduces
`fees0Owed` or `fees1Owed`. Compute each payment once, decrement storage before
external transfers, and transfer only the consumed amounts, as corroborated by
fix commit `8c6b6cca4ed65b22053dc7ffaa0b77d06a160caf`.

---

## [H-02] Liquidation transfers use total token supply and seize excess collateral

### Affected code

- `src/ERC721WrapperBase.sol`: `transfer`, `balanceOf`, and `normalizedToFull`

### Root cause

For every enabled `tokenId`, `transfer` converts a requested unit-of-account
amount into ERC-6909 units with
`amount * totalSupply(tokenId) / balanceOf(sender)`. The numerator uses the
global supply even when the sender owns only a fraction of that `tokenId`.

### Prerequisites and exploit sequence

1. A borrower splits an enabled wrapped position with another account.
2. `balanceOf(sender)` values only the borrower's fractional holdings.
3. During liquidation, `normalizedToFull` nevertheless multiplies by the
   entire `tokenId` supply.
4. The wrapper transfers more ERC-6909 units than correspond to the requested
   value, or reverts when the inflated amount exceeds the borrower's balance.

### Impact

A liquidated borrower can lose more collateral than the liquidator is entitled
to receive. The same inflated calculation can also block liquidation and allow
bad debt to accrue.

### Code evidence and remediation

`ERC721WrapperBase.sol:87-96` loops over every enabled `tokenId` and calls
`normalizedToFull`; lines 176-178 multiply by `totalSupply(tokenId)` rather
than `balanceOf(sender, tokenId)`. Normalize against the sender's per-token
balance, as corroborated by fix commit
`b7549f2700af133ce98a4d6f19e43c857b5ea78a`.

---

## [H-03] Full unwrap strands accrued Uniswap V4 fees after the position exits

### Affected code

- `src/ERC721WrapperBase.sol`: full `unwrap(address,uint256,address)`
- `src/uniswap/UniswapV4Wrapper.sol`: `tokensOwed`, `_accumulateFees`, and `_total`

### Root cause

The full unwrap overload burns the complete ERC-6909 supply and transfers the
underlying NFT without invoking implementation-specific settlement. For
Uniswap V4, previously accumulated fees remain in the wrapper and in
`tokensOwed[tokenId]` after the final holder and the NFT have left.

### Prerequisites and failure sequence

1. A partial unwrap moves outstanding LP fees into the wrapper and records them
   in `tokensOwed[tokenId]`.
2. The final holder calls the three-argument full unwrap.
3. The base contract burns the supply and transfers the NFT without settling
   the recorded fees.
4. If the recipient burns the Uniswap position, the `tokenId` cannot be minted
   again and the fee claim becomes unreachable.

### Impact

The final holder or liquidator permanently loses accrued LP-fee assets, which
remain stuck in the wrapper.

### Code evidence and remediation

`ERC721WrapperBase.sol:69-72` performs only `_burnFrom` and
`underlying.transferFrom`. The V4 implementation tracks fees at
`UniswapV4Wrapper.sol:34` and lines 224-227, but the full unwrap never reads or
clears that state. Add an implementation settlement hook that transfers and
deletes all V4 fee credits, as corroborated by fix commit
`bf5f099b5d73dbff8fa6d403cb54ee6474828ac4`.

---

## [H-04] Floor-rounded liquidation transfers underpay liquidators

### Affected code

- `src/ERC721WrapperBase.sol`: `transfer` and `normalizedToFull`

### Root cause

`normalizedToFull` uses the default floor-rounding form of `Math.mulDiv` when
converting liquidation value into ERC-6909 units. A borrower can leave a
one-unit token balance whose value later increases through fee accrual; a
partial liquidation then rounds that token transfer to zero even though it
represents material collateral value.

### Prerequisites and exploit sequence

1. A borrower enables multiple wrapped positions and reduces one `tokenId` to
   a minimal ERC-6909 balance.
2. Swaps or donations accrue fees to the underlying position.
3. A partial liquidation requests a proportional collateral transfer.
4. Floor rounding transfers zero units of the valuable residual position.
5. The liquidator assumes debt without the corresponding collateral value,
   while the violator retains it.

### Impact

Liquidators suffer a direct collateral shortfall during partial liquidation;
the shortfall can be material when fees substantially increase the value of
the residual unit.

### Code evidence and remediation

`ERC721WrapperBase.sol:176-178` calls the three-argument `Math.mulDiv`, which
rounds down. Round up in favor of the receiver during liquidation, as
corroborated by fix commit
`5e825d5f2eee6789b646bd0f00e9a9a53b5039ca`.
