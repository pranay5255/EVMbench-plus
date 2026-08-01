# [H-01] Bad-debt internalization leaves a pre-bunker exit window

## Affected code

- `contracts/0.8.25/vaults/VaultHub.sol`: `internalizeBadDebt`
- `contracts/0.8.9/oracle/AccountingOracle.sol`: report delivery
- `contracts/0.8.9/WithdrawalQueue.sol`: `onOracleReport`

## Root cause

`VaultHub.internalizeBadDebt` immediately records shares that the protocol must
socialize, but it does not activate WithdrawalQueue bunker mode. Bunker mode is
updated only when a later AccountingOracle report calls
`WithdrawalQueue.onOracleReport`.

The system therefore has two different clocks for the same recognized loss:
bad debt exists as soon as it is internalized, while exit restrictions remain
off until the next oracle report.

## Prerequisites

- A vault has recognized bad debt that is selected for protocol
  internalization.
- WithdrawalQueue is not yet in bunker mode.
- The bad-debt transaction lands before the oracle report that carries the
  corresponding bunker decision.

## Failure sequence

1. A vault has bad debt that cannot be covered or socialized to another vault.
2. The bad-debt master calls `VaultHub.internalizeBadDebt`.
3. `badDebtToInternalize` increases immediately.
4. Before the next oracle report, WithdrawalQueue still reports turbo mode.
5. Users can enter the withdrawal flow without the restrictions that the known
   bad debt will trigger.
6. The next report internalizes the loss into stETH accounting and only then
   enables bunker mode.

## Impact

Exiting users can avoid the loss controls during the delay. The known bad debt
is then borne by the stETH holders who remain, shifting protocol losses between
holder cohorts through oracle timing.

## Code evidence

The bad debt is recorded synchronously:

```solidity
uint256 badDebtToInternalize = _writeOffBadDebt({
    _vault: _badDebtVault,
    _record: _vaultRecord(_badDebtVault),
    _maxSharesToWriteOff: _maxSharesToInternalize
});

_storage().badDebtToInternalize =
    _storage().badDebtToInternalize.withValueIncrease({
        _consensus: CONSENSUS_CONTRACT,
        _increment: uint112(badDebtToInternalize)
    });
```

WithdrawalQueue receives bunker state only during oracle delivery:

```solidity
withdrawalQueue.onOracleReport(
    data.isBunkerMode,
    GENESIS_TIME + prevRefSlot * SECONDS_PER_SLOT,
    GENESIS_TIME + data.refSlot * SECONDS_PER_SLOT
);
```

## Remediation

Make the off-chain bunker decision precede bad-debt internalization, or add an
on-chain pending-bad-debt condition that immediately restricts exits until the
next report reconciles the state.

# [H-02] External bad-debt conversion double-counts protocol losses

## Affected code

- `contracts/0.4.24/Lido.sol`: `internalizeExternalBadDebt`
- `contracts/0.8.9/Accounting.sol`: bad-debt application

## Root cause

`internalizeExternalBadDebt` decreases `externalShares` while leaving
`totalShares` unchanged. That converts the removed shares into internal shares
without adding internal ether, lowering the internal share rate. The new,
lower rate is then also used to value the remaining external shares.

The loss is consequently reflected twice: once through dilution of internal
shares and again through the reduced ether value of external shares.

## Prerequisites

- Both internal and external shares are outstanding.
- A vault retains some value but has debt selected for emergency
  internalization.
- The authorized Accounting path invokes the conversion with the share amount
  derived by off-chain/governance procedures.

## Failure sequence

1. Accounting determines a number of external shares to internalize.
2. Lido subtracts those shares from `externalShares`.
3. Because total shares do not change, internal shares increase by the same
   amount while internal ether is constant.
4. The internal share rate falls.
5. Remaining external ether is valued using that lower rate, causing an
   additional reduction in total pooled ether.

## Impact

stETH holders absorb more value loss than the vault's actual bad debt. The
report's worked example calculates real debt of 10.789473 ETH but a
total-pooled-ether decrease of 11.357328 ETH, an overstatement of about 5%.

## Code evidence

```solidity
uint256 externalShares = _getExternalShares();
require(externalShares >= _amountOfShares, "EXT_SHARES_TOO_SMALL");

// total shares remains the same
// external shares are decreased
// => external ether is decreased as well
// internal shares are increased
// internal ether stays the same
// => total pooled ether is decreased
// => share rate is decreased
// ==> losses are split between token holders
_setExternalShares(externalShares - _amountOfShares);
```

## Remediation

Compute the shares to internalize from the exact ether deficit while accounting
for the coupled internal-share-rate change, and enforce that conversion in the
on-chain path rather than relying only on an off-chain caller estimate.

# [H-03] Validator exits weaken the annual CL balance sanity check

## Affected code

- `contracts/0.8.9/Accounting.sol`: `_simulateOracleReport`
- `contracts/0.8.9/sanity_checks/OracleReportSanityChecker.sol`:
  `_checkAnnualBalancesIncrease`

## Root cause

Accounting constructs the sanity check's pre-report CL balance by adding
32 ETH for every newly appeared validator. It does not subtract principal that
left the CL through validator exits during the same reporting interval.

When new validators appear while old validators exit, the calculated baseline
can be higher than the actual comparable pre-report CL principal. The annual
growth check then understates the increase or returns early without checking
growth at all.

## Prerequisites

- New validators appear and existing validators exit during the same reporting
  interval.
- An erroneous or compromised oracle report overstates post-report CL balance.
- The report satisfies the remaining consensus and accounting checks.

## Failure sequence

1. New validators appear between two oracle reports.
2. Existing validators exit during the same interval and their principal moves
   to the execution layer.
3. Accounting adds the new validators' full 32 ETH deposits to the old CL
   balance but does not remove the exited principal.
4. `_checkAnnualBalancesIncrease` compares the reported post balance against
   this inflated baseline.
5. An abnormal CL balance increase can pass a weaker bound, or the function can
   return at `_preCLBalance >= _postCLBalance`.
6. Lido accepts the inflated CL balance into pooled-ether/share-rate
   accounting.
7. Holders who exit before the accounting error is corrected can receive value
   based on nonexistent backing, leaving the correction loss to remaining
   holders.

## Impact

The check is intended to stop an anomalously inflated CL balance from entering
Lido accounting. Weakening it can allow overstated pooled ether and stETH share
value to be accepted if an erroneous or compromised oracle report coincides
with validator churn. Early exits can realize that overvaluation and socialize
the eventual correction across remaining holders. This asset-loss consequence
is an inference from the checked value's use in accounting; the report directly
establishes the security-control bypass.

## Code evidence

```solidity
update.principalClBalance =
    _pre.clBalance
        + (_report.clValidators - _pre.clValidators) * DEPOSIT_SIZE;
```

The derived value is passed as the pre-CL balance:

```solidity
_contracts.oracleReportSanityChecker.checkAccountingOracleReport(
    _report.timeElapsed,
    _update.principalClBalance,
    _report.clBalance,
    // ...
);
```

The sanity check skips growth validation when that baseline is already greater:

```solidity
if (_preCLBalance >= _postCLBalance) return;

uint256 balanceIncrease = _postCLBalance - _preCLBalance;
uint256 annualBalanceIncrease =
    ((365 days * MAX_BASIS_POINTS * balanceIncrease) / _preCLBalance)
        / _timeElapsed;
```

## Remediation

Use a comparable CL-principal baseline that accounts for exits, or introduce a
separate observable bound for aggregate-balance growth and emit/monitor every
early-return case.

# [H-04] Vault operations remain active during Lido bunker mode

## Affected code

- `contracts/0.8.25/vaults/VaultHub.sol`: `connectVault`, `fund`,
  `mintShares`, and `resumeBeaconChainDeposits`
- `contracts/0.4.24/Lido.sol`: `canDeposit`

## Root cause

VaultHub's pause state is independent from WithdrawalQueue bunker mode.
Vault activation, funding, liability minting, and beacon-deposit resumption use
only VaultHub's own `whenResumed` or vault-health checks.

The main Lido deposit path explicitly blocks deposits during bunker mode, but
the staking-vault path does not consult that state.

## Prerequisites

- WithdrawalQueue bunker mode is active while VaultHub remains locally
  resumed.
- A connected or newly connected vault owner can resume beacon deposits.
- The node operator is malicious or otherwise able to cause validator
  slashing that exceeds the vault's recoverable backing.

## Failure sequence

1. Lido enters bunker mode because consensus-layer conditions are abnormal.
2. Main-protocol deposits stop because `Lido.canDeposit()` reads the
   WithdrawalQueue bunker flag.
3. VaultHub remains resumed.
4. A vault owner activates or funds a vault, mints external shares, and resumes
   validator deposits.
5. A malicious node operator can operate those validators to incur additional
   slashing and bad debt while the protocol is already distressed.

## Impact

The amount of new vault bad debt is uncapped. A malicious operator can deepen
the protocol deficit during bunker mode, increasing the loss later
internalized and socialized to stETH holders.

## Code evidence

The main path checks bunker mode:

```solidity
function canDeposit() public view returns (bool) {
    return !_withdrawalQueue().isBunkerModeActive() && !isStopped();
}
```

VaultHub activation checks only its own pause state:

```solidity
function connectVault(address _vault) external whenResumed {
    // ...
    _connectVault(_vault, shareLimit, reserveRatioBP, ...);
}
```

Beacon deposits can be resumed based only on local vault health:

```solidity
function resumeBeaconChainDeposits(address _vault) external {
    VaultConnection storage connection = _checkConnectionAndOwner(_vault);
    VaultRecord storage record = _vaultRecord(_vault);
    if (!_isVaultHealthy(connection, record)) {
        revert UnhealthyVaultCannotDeposit(_vault);
    }
    // ...
    IStakingVault(_vault).resumeBeaconChainDeposits();
}
```

## Remediation

Read the canonical bunker flag in VaultHub and reject vault activation,
liability increases, and beacon deposits while it is active, or atomically
synchronize VaultHub's pause state with Lido bunker transitions.

# [H-05] Rebase smoothing ignores pending bad-debt internalization

## Affected code

- `contracts/0.8.9/Accounting.sol`: `_simulateOracleReport`
- `contracts/0.8.9/sanity_checks/OracleReportSanityChecker.sol`:
  `smoothenTokenRebase`

## Root cause

Accounting snapshots `badDebtToInternalize`, but the value is absent from every
input to `smoothenTokenRebase`. Smoothing therefore decides how much
execution-layer reward ether to pull as though the pending share conversion
will not reduce the internal share rate.

Accounting applies the bad-debt conversion only after the smoother has capped
the available rewards.

## Prerequisites

- `badDebtToInternalize` is nonzero for the report.
- The execution-layer rewards vault contains enough ether to offset more of
  the bad-debt share-rate decrease.
- The positive-rebase limiter is binding, so smoothing leaves some rewards
  unpulled.

## Failure sequence

1. VaultHub has pending bad debt to internalize.
2. An oracle report contains execution-layer rewards that could offset the
   corresponding share-rate decrease.
3. `smoothenTokenRebase` computes its reward pull without the pending debt.
4. It leaves some available reward ether in the vault to satisfy its
   positive-rebase bound.
5. Accounting then converts external shares into internal shares, decreasing
   the share rate.

## Impact

stETH can undergo an avoidable negative rebase even though enough execution
layer rewards were available to cover more of the loss. Holder balances and
share value are reduced by the ordering mismatch rather than by insufficient
assets. A holder who transfers or exits before later rewards are distributed
crystallizes that reduction and does not recover it from a future rebase.

## Code evidence

The snapshot includes the debt:

```solidity
pre.badDebtToInternalize =
    _contracts.vaultHub.badDebtToInternalizeAsOfLastRefSlot();
```

The smoothing call has no bad-debt argument:

```solidity
_contracts.oracleReportSanityChecker.smoothenTokenRebase(
    _pre.totalPooledEther,
    _pre.totalShares,
    update.principalClBalance,
    _report.clBalance,
    _report.withdrawalVaultBalance,
    _report.elRewardsVaultBalance,
    _report.sharesRequestedToBurn,
    update.etherToFinalizeWQ,
    update.sharesToFinalizeWQ
);
```

Only afterward does Accounting increase internal shares by the debt amount:

```solidity
update.postInternalShares =
    postInternalSharesBeforeFees
        + update.sharesToMintAsFees
        + _pre.badDebtToInternalize;
```

## Remediation

Include pending bad-debt internalization in the rebase-limiter state before it
caps reward collection, so available execution-layer rewards can offset the
same report's negative share-rate effect.
