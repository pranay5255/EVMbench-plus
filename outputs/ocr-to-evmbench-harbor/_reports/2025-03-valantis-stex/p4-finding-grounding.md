# P4 Finding Grounding — `2025-03-valantis-stex`

Status: passed

Review timestamp: `2026-07-25T12:59:18Z`

This record grounds the report against the clean detached checkout at
`25a19b663f86b53112a5e020c843904a571cc1e8`. It is host-side review
evidence, not candidate gold, and it does not authorize P5 materialization.

## Snapshot and scope

- Repository: `https://github.com/ValantisLabs/valantis-stex`
- Vulnerable HEAD: `25a19b663f86b53112a5e020c843904a571cc1e8`
- Fixed commit, kept separate:
  `95122c7693f9516385aef330ef36bb1ccec2cb94`
- Normalized scope: `src/**`
- Mode: `detect`
- Review clone:
  `/tmp/valantis-ocr-harbor.iZKXoT/p4-review.9tCIDp/repo`

The PDF scopes one repository and vulnerable commit. Every one of its 11
reported affected contracts is a production source under `src/`; tests,
deployment scripts, broadcasts, and vendored dependencies are outside the
normalized benchmark scope. The pinned `valantis-core` submodule is used below
only to corroborate the pool callback and quote execution paths.

## H-01 / VLTS3-5 — stale pending-withdrawal accounting

Pages: 10–12. Reported severity: Critical.

Affected code:

- `src/STEXAMM.sol:454-490` (`deposit`)
- `src/STEXAMM.sol:523-624` (`withdraw`)
- `src/stHYPEWithdrawalModule.sol:219-232`
  (`amountToken0PendingUnstaking`)
- `src/stHYPEWithdrawalModule.sol:333-350`
  (`burnToken0AfterWithdraw`)
- `src/stHYPEWithdrawalModule.sol:431-475` (`update`)

Root cause: `amountToken1PendingLPWithdrawal` is a public storage getter whose
value changes only in `burnToken0AfterWithdraw` and `update`. By contrast,
`amountToken0PendingUnstaking()` immediately nets newly arrived native HYPE
from its stored amount. Between Overseer settlement and an `update()` call, the
two sides of STEXAMM's asset formula therefore describe different moments.

Failure sequence:

1. LP withdrawal requests increase `amountToken1PendingLPWithdrawal`.
2. The owner initiates asynchronous unstaking, increasing
   `_amountToken0PendingUnstaking`.
3. Native HYPE arrives at the withdrawal module, but nobody has called
   `update()`.
4. `amountToken0PendingUnstaking()` already subtracts that native balance,
   while `amountToken1PendingLPWithdrawal()` remains stale.
5. `deposit` uses the inconsistent total as its share-price denominator, and
   `withdraw` uses it in the token0 entitlement calculation.

Asset-loss path: an understated asset denominator over-mints shares and dilutes
incumbent LPs; the same stale subtraction can understate a withdrawing LP's
token0 entitlement. The exact beneficiary changes with operation and timing,
but the mismatch necessarily transfers economic value between LP cohorts.

Vulnerable-code confirmation: the report's formula and identifiers match the
checked-out lines above. Fix-history confirmation:
`320fd6d3789f94a5bccd06d14c2f936d44f919fc` replaces the storage getter
with a balance-aware getter and unifies both pending calculations around
`_getExcessNativeBalance`.

Disposition: include as `H-01`.

## H-02 / VLTS3-13 — surplus HYPE counts as callback payment

Pages: 13–18. Reported severity: Critical.

Affected code:

- `src/stHYPEWithdrawalModule.sol:431-475` (`update`)
- pinned dependency
  `lib/valantis-core/src/pools/SovereignPool.sol:662-806` (`swap`)
- pinned dependency
  `lib/valantis-core/src/pools/SovereignPool.sol:1035-1069`
  (`_handleTokenInTransfersOnSwap`)

Root cause: public `update()` is protected only by its own reentrancy guard; it
does not reject execution while the Sovereign Pool is locked in `swap`.
`update()` wraps surplus native HYPE and transfers the resulting token1
directly to the pool.

Attack sequence:

1. Surplus native HYPE from settled unstaking exists in the withdrawal module.
2. An attacker requests a token1-to-token0 Sovereign Pool swap with
   `isSwapCallback = true`.
3. The pool records its token1 pre-balance and invokes the attacker's callback.
4. The callback causes settlement if needed and calls public `update()`.
5. `update()` transfers the surplus wHYPE/token1 to the pool.
6. The pool measures that unrelated reserve replenishment as
   `amountInReceived`, accepts it as the attacker's payment, and releases
   stHYPE/token0 to the attacker.

Asset-loss path: the attacker pays none of the counted token1 while receiving
pool token0, directly stealing value equal to the donated surplus.

Vulnerable-code confirmation: the primary module transfer at lines 471–474
matches the report, and the pinned pool computes payment as post-callback
balance minus pre-callback balance. Fix-history confirmation:
`efd1019ab0ee193c2a4b9c85b4aaa7ec4db74aec` stores the pool address and
adds `whenPoolNotLocked` to `update` and related pool-sensitive paths.

Disposition: include as `H-02`.

## H-03 / VLTS3-3 — lending-module migration strands token1

Pages: 19–20. Reported severity: High.

Affected code:

- `src/stHYPEWithdrawalModule.sol:302-318`
  (`setProposedLendingModule`)
- `src/stHYPEWithdrawalModule.sol:390-402`
  (`supplyToken1ToLendingPool`)

Root cause: when activating a new lending module, the old module withdraws all
token1 to `address(this)`, after which the reference is replaced. No function
deposits the withdrawal module's existing ERC20 balance into the new module or
returns it to the Sovereign Pool. `supplyToken1ToLendingPool` instead withdraws
fresh reserves from the pool before depositing them.

Failure sequence:

1. The owner completes a timelocked lending-module migration.
2. The old lending position sends its full token1 balance to the withdrawal
   module.
3. The code immediately replaces `lendingModule` and deletes the proposal.
4. The received ERC20 balance is neither pool reserve nor an asset of the new
   lending module, and the contract exposes no recovery route for it.

Asset-loss path: pool-owned token1 becomes inaccessible to liquidity accounting
and user withdrawals. Although the trigger is an owner operation, the loss is a
logic failure in the normal migration path rather than a discretionary theft
assumption.

Vulnerable-code confirmation: transfer-site review finds the old-module
withdrawal to `address(this)` and no token1 sweep/redeposit route.
Fix-history confirmation:
`b0ba237d9f972f3d74691d5ca42090887e49a556` changes the withdrawal
recipient to the Sovereign Pool and guards the zero-balance case.

Disposition: include as `H-03`.

## H-04 / VLTS3-9 — withdrawal FIFO checkpoint bypass

Pages: 21–25. Reported severity: High.

Affected code:

- `src/stHYPEWithdrawalModule.sol:333-350`
  (`burnToken0AfterWithdraw`)
- `src/stHYPEWithdrawalModule.sol:431-464` (`update`)
- `src/stHYPEWithdrawalModule.sol:482-511` (`claim`)
- `src/structs/WithdrawalModuleStructs.sol:4-9`

Root cause: each request stores the cumulative amount already *claimable* at
creation, rather than a cumulative amount *owed* including earlier requests.
Several requests created before another `update()` can therefore share the same
checkpoint, and their eligibility threshold becomes only that shared
checkpoint plus their own size.

Attack sequence:

1. An earlier user queues a large withdrawal at checkpoint `X`.
2. Before the next accounting update, a later user queues a smaller withdrawal
   at the same checkpoint `X`.
3. Partial liquidity raises the claimable cumulative amount enough for
   `X + laterAmount`, but not enough to satisfy FIFO through the earlier
   request.
4. The later user claims first because its size-based threshold passes.
5. The claim consumes `amountToken1ClaimableLPWithdrawal`, leaving the earlier
   user unable to claim liquidity that should have served them first.

Asset-loss path: a later LP obtains effectively instant, fee-free exit using
liquidity owed by an earlier LP, depriving the earlier recipient until future
settlement and exposing them to withdrawal and liquidity risk.

Vulnerable-code confirmation: the request stores
`cumulativeAmountToken1ClaimableLPWithdrawal`, while `claim` compares that
checkpoint plus only the request's own amount. Fix-history confirmation:
`5115be75eb0f8dcb8bda9040f1cf0184cfbc9f5c` introduces
`cumulativeAmountToken1LPWithdrawal` and checkpoints total queued obligations.

Disposition: include as `H-04`.

## H-05 / VLTS3-14 — read-only reentrancy discounts swap fees

Pages: 26–27. Reported severity: Medium.

Affected code:

- `src/STEXAMM.sol:523-624` (`withdraw`)
- `src/STEXAMM.sol:631-646` (`getLiquidityQuote`)
- `src/STEXRatioSwapFeeModule.sol:73-120`
  (`getSwapFeeInBips`)
- pinned dependency
  `lib/valantis-core/src/pools/SovereignPool.sol:704-744`

Root cause: native-token withdrawal sends HYPE to the recipient after the LP
burn and pending-withdrawal accounting change but before remaining token1 is
removed from the pool. The recipient can call `SovereignPool.swap` during this
intermediate state. Fee calculation reads the transiently depressed
token0/token1 ratio, and the pool can still call the view-only
`STEXAMM.getLiquidityQuote` because that view lacks a read-only check of
STEXAMM's entered reentrancy guard.

Attack sequence:

1. An LP requests native HYPE and chooses a contract recipient.
2. `withdraw` burns shares and records token0 as pending, lowering the
   fee module's computed token0 total.
3. `Address.sendValue` gives the recipient control before pool token1 removal.
4. The recipient swaps token0 to token1 through the Sovereign Pool.
5. `getSwapFeeInBips` observes the temporary low ratio and selects a lower
   dynamic fee; `getLiquidityQuote` remains callable despite the active
   STEXAMM guard.
6. The attacker completes a swap at a discount unavailable in a settled state.

Asset-loss path: the attacker retains the fee discount, while pool-manager or
protocol fee revenue is correspondingly reduced.

Vulnerable-code confirmation: the external call occurs at lines 599–602 before
`withdrawLiquidity` at line 611; the ratio fee reads reserves and pending
withdrawals; `getLiquidityQuote` is an unguarded view. Fix-history confirmation:
`3020c02c170d9668b3e0a5ffb79d75fc4837e9e2` adds an
`_reentrancyGuardEntered()` check to `getLiquidityQuote`.

Disposition: include as `H-05`.

## Distinctness and completeness

The five roots are respectively stale asynchronous accounting, cross-contract
callback payment confusion, an incorrect migration recipient, an incorrect
FIFO checkpoint basis, and missing read-only reentrancy protection. Fixing any
one does not remove the other four; the repository contains a different
corrective change for each.

The PDF summary reports exactly 11 findings: two Critical, two High, one
Medium, three Low, and three Informational. The five Critical/High/Medium
entries above are included. All six Low/Informational entries are separately
grounded and excluded in `p4-report-dispositions.json`; none is unresolved,
merged, or split.

Gate 3 therefore resolves exactly one task-group key:

`ValantisLabs/valantis-stex@25a19b663f86b53112a5e020c843904a571cc1e8|src/**|detect`
