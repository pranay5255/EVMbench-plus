# [H-01] Inverted redeem-demand conversion corrupts oracle prices and redistributes vault assets

## Affected code

- `src/oracles/OracleHelper.sol`: `AssetPrice`, `getPricesD18`
- Downstream value movement: `src/queues/DepositQueue.sol::_claim`,
  `src/queues/DepositQueue.sol::_handleReport`, and
  `src/queues/RedeemQueue.sol::_handleReport`

## Root cause

`OracleHelper.AssetPrice.priceD18` defines the value of one non-base asset in
base-asset units. For example, `priceD18 == 2e18` means that one unit of the
asset is worth two units of the base asset. A non-base withdrawal demand must
therefore be multiplied by `priceD18` to express it in base-asset units.

At audited commit `60c462d6b006b19790b07c009b7a48aa3bcb3e96`,
`getPricesD18` performs the inverse conversion:

```solidity
if (assetPrice.priceD18 == 0) {
    $.totalRedeemDemand += demand_;
} else {
    $.totalRedeemDemand += Math.mulDiv(demand_, 1 ether, assetPrice.priceD18);
}
```

The incorrectly converted demand is subtracted from `totalAssets` when the
base share price is calculated. The function then derives every non-base price
from that already-corrupted base price. This is internally inconsistent with
the function's final conversion, which correctly multiplies the base price by
the relative asset price.

## Preconditions

- The vault has a live redeem queue for a non-base asset with pending demand.
- The non-base asset's relative `priceD18` differs from `1e18`.
- A keeper uses `OracleHelper.getPricesD18` to prepare a report, and a caller
  with `SUBMIT_REPORTS_ROLE` submits a report that passes the oracle's
  deviation/suspicion checks (or is subsequently accepted by the authorized
  report-acceptance path).

The oracle submission path is permissioned; this finding does not assume that
an arbitrary caller can directly write an oracle price.

## Failure and value-transfer sequence

1. Users place redemption demand in a non-base queue.
2. The helper converts that demand with division instead of multiplication.
   For `demand_ = 1e18` and `priceD18 = 2e18`, the correct base-asset demand is
   `2e18`, but the vulnerable code records `0.5e18`: a `1.5e18`
   understatement and a fourfold ratio error.
3. The understated demand leaves the helper's net-asset denominator too high,
   so `totalShares / netAssets` produces a price that is too low in
   shares-per-asset terms. The error propagates to every returned asset price.
4. Once the report is accepted, deposit queues mint shares as
   `assets * priceD18`, while redeem queues pay assets as
   `shares / priceD18`. A price that is too low gives depositors fewer shares
   for their assets and gives withdrawing users more assets for their shares.

The direction reverses for relative prices below one, but the invariant breach
is the same: participants are settled at an incorrect exchange rate, moving
value between vault users and depleting assets available to the disadvantaged
side.

## Impact

Direct economic loss through incorrect deposit and redemption settlement. The
report specifically identifies incorrect vault valuation, unfair distribution
of funds on withdrawal, and potential financial exploitation. The source code
shows how the malformed helper price reaches the queue formulas that mint
shares and release underlying assets.

## Remediation evidence

Final report commit `72f689f965e4ac1a4c2bcfb645a8b5416cf740c7`
replaces the inverted conversion with multiplication:

```solidity
totalAssets -= Math.mulDiv(demand_, assetPrice.priceD18, 1 ether);
```

That final commit is remediation evidence only and is not the vulnerable task
snapshot.
