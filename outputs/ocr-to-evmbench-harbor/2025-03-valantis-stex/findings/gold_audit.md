# [H-01] Stale pending-withdrawal accounting misprices LP shares

## Affected code

- `src/STEXAMM.sol`: `deposit` and `withdraw`
- `src/stHYPEWithdrawalModule.sol`: `amountToken0PendingUnstaking`,
  `burnToken0AfterWithdraw`, and `update`

## Root cause

STEXAMM values LP shares using two pending-withdrawal quantities that observe
different accounting states. `amountToken1PendingLPWithdrawal` is a public
storage getter and changes only when a request is created or `update()` runs.
`amountToken0PendingUnstaking()`, however, immediately subtracts newly arrived
native HYPE from `_amountToken0PendingUnstaking`.

After the Overseer sends HYPE but before `update()` executes, the token0 side
has already incorporated settlement while the token1 liability remains stale.
Both `deposit` and `withdraw` then price shares from an internally inconsistent
asset total.

## Failure sequence

1. LP withdrawals increase `amountToken1PendingLPWithdrawal`.
2. The owner initiates asynchronous stHYPE unstaking, increasing
   `_amountToken0PendingUnstaking`.
3. The Overseer sends native HYPE to the withdrawal module.
4. Before `update()` is called, `amountToken0PendingUnstaking()` nets the new
   HYPE balance but `amountToken1PendingLPWithdrawal()` still returns its old
   value.
5. A deposit or withdrawal uses the mismatched values in its share formula.

## Impact

When the stale liability understates the denominator, a depositor receives too
many shares and dilutes existing LPs. The same stale subtraction can reduce a
withdrawing LP's token0 entitlement. Value is transferred between LP cohorts
solely according to settlement and keeper timing.

## Code evidence

`STEXAMM.deposit` subtracts the stored pending token1 amount from a total whose
pending token0 component is already balance-aware:

```solidity
(uint256 reserve0Pool, uint256 reserve1Pool) =
    ISovereignPool(pool).getReserves();
uint256 reserve0Total =
    reserve0Pool + _withdrawalModule.amountToken0PendingUnstaking();
uint256 reserve1PendingWithdrawal =
    _withdrawalModule.amountToken1PendingLPWithdrawal();

shares = Math.mulDiv(
    _amount,
    totalSupplyCache,
    reserve1Pool + _withdrawalModule.amountToken1LendingPool()
        + _withdrawalModule.convertToToken1(reserve0Total)
        - reserve1PendingWithdrawal
);
```

The token0 getter immediately observes native HYPE that arrived since the last
state update:

```solidity
uint256 balanceNative = address(this).balance;
uint256 excessNative =
    balanceNative > amountToken1ClaimableLPWithdrawal
        ? balanceNative - amountToken1ClaimableLPWithdrawal
        : 0;

if (_amountToken0PendingUnstaking > excessNative) {
    return _amountToken0PendingUnstaking - excessNative;
}
return 0;
```

There is no equivalent balance-aware getter for the vulnerable
`amountToken1PendingLPWithdrawal` storage variable.

## Remediation

Calculate both pending quantities from the same excess-native-balance snapshot,
or force the accounting update before any share-price operation. The fixed
implementation introduces a balance-aware token1 getter and a shared
`_getExcessNativeBalance()` calculation.
# [H-02] Swap callback can steal unstaking surplus

## Affected code

- `src/stHYPEWithdrawalModule.sol`: `update`
- Pinned `valantis-core`: `SovereignPool.swap` and
  `_handleTokenInTransfersOnSwap`

## Root cause

The public `update()` function uses only the withdrawal module's local
reentrancy guard. It does not reject execution while the Sovereign Pool is
locked inside a swap. When surplus native HYPE exists, `update()` wraps it and
transfers token1 directly to the pool.

For callback-funded swaps, the pool treats any token balance increase during
the callback as payment from the caller. It cannot distinguish the withdrawal
module's reserve replenishment from attacker-funded input.

## Attack sequence

1. Settled unstaking leaves surplus native HYPE in the withdrawal module.
2. An attacker starts a token1-to-token0 Sovereign Pool swap with the payment
   callback enabled.
3. The pool records its token1 balance and calls the attacker's callback.
4. The attacker calls public `update()` during that callback.
5. `update()` wraps the surplus and transfers the resulting token1 to the pool.
6. The pool observes the balance increase, accepts it as the attacker's input,
   and sends stHYPE/token0 to the attacker.

## Impact

The attacker receives pool token0 without supplying the token1 counted as
payment. The entire available surplus can be converted into attacker-owned
assets, directly stealing pool value.

## Code evidence

The vulnerable update donates the surplus directly:

```solidity
token1.deposit{value: balanceSurplus}();
token1.safeTransfer(stexInterface.pool(), balanceSurplus);
```

The pinned pool measures callback payment only as a balance delta:

```solidity
uint256 preBalance = token.balanceOf(sovereignVault);

if (isSwapCallback) {
    ISovereignPoolSwapCallback(msg.sender).sovereignPoolSwapCallback(
        address(token), amountInUsed, _swapCallbackContext
    );
}

uint256 amountInReceived =
    token.balanceOf(sovereignVault) - preBalance;
```

`update()` is unrestricted and has no Sovereign Pool lock check in the
vulnerable snapshot.

## Remediation

Reject `update()` and any equivalent reserve transfer while
`SovereignPool.isLocked()` is true, or route replenishment through a
non-reentrant pool donation primitive. The fixed implementation stores the pool
address and applies a `whenPoolNotLocked` guard.
# [H-03] Lending-module migration strands withdrawn token1

## Affected code

- `src/stHYPEWithdrawalModule.sol`: `setProposedLendingModule` and
  `supplyToken1ToLendingPool`

## Root cause

Activating a proposed lending module withdraws the old module's entire token1
position to `address(this)`. The function then replaces the module reference
without transferring that ERC20 balance to the Sovereign Pool or depositing it
into the replacement module.

The remaining supply function cannot recover the balance: it first pulls fresh
token1 reserves out of the pool and deposits only that requested amount.
No function sweeps token1 already held by the withdrawal module.

## Failure sequence

1. The owner proposes a new lending module and waits for the timelock.
2. `setProposedLendingModule()` withdraws the old module's full position to the
   withdrawal module.
3. The function immediately replaces `lendingModule` and deletes the proposal.
4. The withdrawn token1 is not reserve in the Sovereign Pool and is not owned
   by the new lending position.
5. No exposed path can return or redeposit that existing balance.

## Impact

Pool-owned token1 becomes inaccessible to reserve accounting and user
withdrawals. A normal administrative migration can therefore strand the full
old lending position and leave LP assets unusable.

## Code evidence

```solidity
if (address(lendingModule) != address(0)) {
    lendingModule.withdraw(
        lendingModule.assetBalance(),
        address(this)
    );
}

lendingModule =
    ILendingModule(lendingModuleProposal.lendingModule);
delete lendingModuleProposal;
```

The only path that supplies the new module takes fresh assets from the pool:

```solidity
stexInterface.supplyToken1Reserves(_amountToken1);
IWETH9(token1).forceApprove(address(lendingModule), _amountToken1);
lendingModule.deposit(_amountToken1);
```

## Remediation

Withdraw the old lending position directly to the Sovereign Pool so it becomes
reserve immediately, then explicitly supply any desired amount from the pool
to the replacement module. The fixed implementation uses the pool as the
withdrawal recipient.
# [H-04] Withdrawal checkpoints let later claims bypass FIFO

## Affected code

- `src/stHYPEWithdrawalModule.sol`: `burnToken0AfterWithdraw`, `update`, and
  `claim`
- `src/structs/WithdrawalModuleStructs.sol`: `LPWithdrawalRequest`

## Root cause

Each withdrawal request stores
`cumulativeAmountToken1ClaimableLPWithdrawal`, the amount already fulfilled at
creation. It does not checkpoint cumulative queued obligations. Multiple
requests created before another settlement update can therefore receive the
same checkpoint.

Eligibility is then checked as that shared checkpoint plus only the request's
own size. A later small request becomes eligible before an earlier large
request even though FIFO requires all earlier obligations to be funded first.

## Attack sequence

1. User 1 queues a large withdrawal at fulfilled checkpoint `X`.
2. Before another update, User 2 queues a smaller withdrawal at the same
   checkpoint `X`.
3. Partial settlement makes cumulative fulfilled liquidity exceed
   `X + User2Amount` but not the total obligations through User 1.
4. User 2's claim passes and consumes claimable HYPE.
5. User 1's earlier claim fails because the remaining claimable balance is
   insufficient.

## Impact

A later LP obtains an effectively instant, fee-free exit using liquidity that
FIFO reserves for an earlier LP. The earlier recipient loses access to their
funds until further settlement and bears the resulting liquidity and timing
risk.

## Code evidence

All requests created before the next update can store the same value:

```solidity
LPWithdrawals[idLPWithdrawal] = LPWithdrawalRequest({
    recipient: _recipient,
    amountToken1: amountToken1.toUint96(),
    cumulativeAmountToken1ClaimableLPWithdrawalCheckpoint:
        cumulativeAmountToken1ClaimableLPWithdrawal
});
```

The claim threshold then depends only on the request's own amount:

```solidity
if (
    cumulativeAmountToken1ClaimableLPWithdrawal
        < request.cumulativeAmountToken1ClaimableLPWithdrawalCheckpoint
            + request.amountToken1
) {
    revert stHYPEWithdrawalModule__claim_cannotYetClaim();
}

amountToken1ClaimableLPWithdrawal -= request.amountToken1;
```

## Remediation

Checkpoint cumulative token1 obligations when requests are created, and allow
a request only after cumulative fulfilled liquidity reaches that request's
position in the owed queue. The fixed implementation introduces
`cumulativeAmountToken1LPWithdrawal`.
# [H-05] Withdrawal read-only reentrancy discounts swap fees

## Affected code

- `src/STEXAMM.sol`: `withdraw` and `getLiquidityQuote`
- `src/STEXRatioSwapFeeModule.sol`: `getSwapFeeInBips`
- Pinned `valantis-core`: `SovereignPool.swap`

## Root cause

When an LP requests native HYPE, `withdraw()` calls the recipient after burning
shares and recording the token0 withdrawal but before removing the remaining
token1 from the Sovereign Pool. The callback recipient can start a pool swap
while STEXAMM exposes this intermediate reserve/liability ratio.

The dynamic fee module reads the transient ratio. The pool then calls
view-only `STEXAMM.getLiquidityQuote`, which does not check whether STEXAMM's
reentrancy guard is already entered. The swap can therefore complete while the
outer withdrawal remains in progress.

## Attack sequence

1. An LP withdraws to a contract recipient with native-token unwrapping.
2. STEXAMM burns the LP shares and records token0 as a pending withdrawal.
3. `Address.sendValue` gives the recipient control before linearly subsequent
   pool token1 removal.
4. The recipient performs a token0-to-token1 Sovereign Pool swap.
5. `getSwapFeeInBips` observes a temporarily depressed token0/token1 ratio and
   chooses a lower dynamic fee.
6. Unguarded `getLiquidityQuote` remains callable, so the discounted swap
   completes before the outer withdrawal restores a settled state.

## Impact

The callback trader retains the fee discount while the pool manager or protocol
collects less fee revenue than the same swap would owe in a settled state.
Repeated use leaks protocol revenue to the attacker.

## Code evidence

The recipient callback precedes pool token1 removal:

```solidity
if (_unwrapToNativeToken) {
    IWETH9(token1).withdraw(cache.amount1LendingPool);
    Address.sendValue(
        payable(_recipient),
        cache.amount1LendingPool
    );
}

// Executed later
ISovereignPool(pool).withdrawLiquidity(
    0,
    cache.amount1Remaining,
    msg.sender,
    address(this),
    new bytes(0)
);
```

The fee uses live reserves and the newly changed pending liability:

```solidity
uint256 amount0Total =
    reserve0 + amount0PendingUnstaking + _amountIn
        - amountToken0PendingLPWithdrawal;
uint256 reserve1Total =
    reserve1 + withdrawalModuleInterface.amountToken1LendingPool();
uint256 ratioBips = (amount0Total * BIPS) / reserve1Total;
```

The vulnerable quote function is an unguarded external view:

```solidity
function getLiquidityQuote(...)
    external
    view
    override
    returns (ALMLiquidityQuote memory quote)
{
    quote.amountInFilled = _almLiquidityQuoteInput.amountInMinusFee;
    // ...
}
```

## Remediation

Make every view path used by a swap reject execution while STEXAMM's
reentrancy guard is entered. The fixed implementation checks
`_reentrancyGuardEntered()` at the start of `getLiquidityQuote`.
