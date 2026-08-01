# Hemi VUSD detect findings

# [H-01] Keeper-controlled zero output floor exposes protocol rewards to sandwiches

## Affected code

- `contracts/Treasury.sol`: `claimCompAndConvertTo`

## Root cause

`claimCompAndConvertTo` swaps the Treasury's full COMP reward balance while
accepting `_minOut` entirely from a keeper or governor. The contract does not
enforce a nonzero or protocol-derived output floor before forwarding that
value to `swapExactTokensForTokens`.

The router quote returned as `amountOut` is used only to decide whether to
enter the swap branch. It is not used to constrain the executed output.

## Prerequisites

- A keeper or governor submits the reward-conversion transaction with
  `_minOut == 0` or another economically unsafe value.
- An attacker can observe and sandwich the public transaction, or a
  compromised keeper coordinates with the price manipulation.
- The selected route has enough manipulable liquidity for the attacker to
  move its execution price.

## Exploit sequence

1. The Treasury claims all available COMP rewards.
2. A keeper broadcasts `claimCompAndConvertTo` with a zero output floor.
3. An attacker front-runs the transaction and moves the selected pool price
   against the Treasury.
4. The Treasury's swap remains valid for any nonzero output and sells the
   entire COMP balance at the manipulated rate.
5. The attacker reverses the price movement after the Treasury trade and
   retains the extracted value.

## Impact

Protocol-owned COMP rewards can be exchanged for a negligible amount of the
destination asset. The lost yield would otherwise be deposited into Compound
and support the VUSD system.

## Code evidence

The caller controls `_minOut`, while `amountOut` from the route search is not
used as the minimum:

```solidity
function claimCompAndConvertTo(address _toToken, uint256 _minOut)
    external
    onlyKeeperOrGovernor
{
    // ...
    (address[] memory path, uint256 amountOut, uint256 rIdx) =
        swapManager.bestOutputFixedInput(COMP, _toToken, _compAmount);
    if (amountOut != 0) {
        swapManager.ROUTERS(rIdx).swapExactTokensForTokens(
            _compAmount,
            _minOut,
            path,
            address(this),
            block.timestamp
        );
    }
}
```

## Remediation

Reject zero and economically unsafe minimums. Prefer deriving a protocol-side
floor from the route quote and a tightly bounded slippage policy rather than
relying only on the privileged caller to supply one.

# [H-02] Nominal fee-on-transfer accounting mints unbacked VUSD

## Affected code

- `contracts/Minter.sol`: `_mint` and `_calculateMintage`

## Root cause

`_mint` calculates VUSD issuance from the caller's nominal `_amountIn` before
transferring the collateral. It never measures the Minter's balance change.
If a whitelisted ERC-20 deducts a transfer fee, less collateral arrives than
the amount used to calculate `_mintage`.

## Prerequisites

- A whitelisted collateral token deducts a transfer fee or otherwise credits
  less than the requested transfer amount.
- Its oracle price remains within the configured stable-price tolerance.
- A public caller approves the Minter and deposits that token.

## Exploit sequence

1. A user calls a public `mint` overload with a nominal collateral amount.
2. `_calculateMintage` computes VUSD output from that full nominal amount.
3. `safeTransferFrom` succeeds but the token credits the Minter with less
   collateral after deducting its fee.
4. The Minter deposits the smaller received balance into Compound.
5. It nevertheless mints the larger nominal VUSD amount to the caller.
6. Repeated mints create undercollateralized VUSD that can be redeemed against
   other assets held by the shared Treasury.

## Impact

The attacker receives more VUSD than the deposited collateral supports and
can externalize the deficit onto other VUSD holders or Treasury collateral.
At scale, honest redemptions become underfunded.

## Code evidence

The nominal amount is priced before the transfer:

```solidity
_mintage = _calculateMintage(_token, _amountIn);
IERC20(_token).safeTransferFrom(_msgSender(), address(this), _amountIn);
```

The contract then deposits its actual balance but mints the already-computed
nominal output:

```solidity
address _cToken = cTokens[_token];
require(
    CToken(_cToken).mint(IERC20(_token).balanceOf(address(this))) == 0,
    "cToken-mint-failed"
);
IERC20(_cToken).safeTransfer(
    treasury(),
    IERC20(_cToken).balanceOf(address(this))
);
vusd.mint(_receiver, _mintage);
```

The immediate post-audit fix at
`f3dec329d42c6e6b81ea61c3f4f4dd3340e976e2` instead measures
`balanceAfter - balanceBefore` and calculates issuance from that delta.

## Remediation

Measure the exact balance increase across `safeTransferFrom` and calculate
VUSD issuance from the received amount. Deposit only that transaction's
balance delta, or explicitly reject tokens whose received amount differs from
the requested amount.

# [H-03] Always-current router deadlines give validators indefinite execution optionality

## Affected code

- `contracts/Treasury.sol`: `claimCompAndConvertTo`

## Root cause

The Treasury passes `block.timestamp` as the Uniswap-style router deadline.
Because that expression is evaluated only when the transaction executes, it
is always equal to the current block time and can never reject an old pending
transaction.

This is separate from the output-floor issue: a nonzero `_minOut` limits the
absolute output but does not bound how long validators or builders may wait
for the most adverse still-valid execution point.

## Prerequisites

- A keeper or governor broadcasts a COMP conversion transaction.
- A validator, builder, or other party with ordering influence can delay its
  inclusion.
- The caller's `_minOut` leaves an economically exploitable price interval.

## Failure sequence

1. The keeper prepares the swap using current market conditions.
2. A block producer withholds the transaction instead of including it
   promptly.
3. Market conditions later move to the least favorable point that still
   satisfies `_minOut`.
4. The producer includes the stale transaction.
5. The router sees `deadline == block.timestamp`, so the age of the original
   transaction provides no reason to revert.

## Impact

Protocol reward conversion can execute much later than intended at an
adversely selected price, transferring value from the Treasury to arbitrageurs
or ordered-flow participants up to the caller's allowed slippage.

## Code evidence

The deadline has no relationship to the transaction's creation time:

```solidity
swapManager.ROUTERS(rIdx).swapExactTokensForTokens(
    _compAmount,
    _minOut,
    path,
    address(this),
    block.timestamp
);
```

## Remediation

Accept a caller-supplied expiry representing the keeper's signing or
submission intent, enforce that it is within a short protocol-defined horizon,
and pass that fixed value to the router.
