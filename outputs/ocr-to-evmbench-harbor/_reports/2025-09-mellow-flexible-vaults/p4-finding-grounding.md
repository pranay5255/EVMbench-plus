# H-01 code and economic grounding

The source report defines `priceD18` as a multiplier: `2e18` means one unit of
the non-base asset is worth two base-asset units. At selected commit
`60c462d6...`, `OracleHelper.getPricesD18` instead computes
`demand_ * 1e18 / priceD18` for non-base redeem demand. With a demand of one
asset and a relative price of two, this returns `0.5` base assets instead of
`2`, understating demand by `1.5` and producing a fourfold ratio error.

The malformed demand is subtracted from total assets before the base price is
computed as shares divided by net assets. Understating demand leaves the
denominator too large and the shares-per-asset price too low. The helper then
multiplies this base price by each relative asset price, so the error reaches
all returned prices.

The economic sink is executable source, not report prose alone:

- Deposit queues use `assets * priceD18` to mint/allocate shares.
- Redeem queues use `shares / priceD18` to determine released assets.

After an authorized report is accepted, a price that is too low under-issues
deposit shares and overpays redemption assets. A relative price below one
causes the opposite directional error, but still settles one side at the
expense of another. The report independently characterizes the outcome as
incorrect valuation, unfair fund distribution on withdrawal, and potential
financial exploitation.

The oracle is permissioned and applies validation/suspicion thresholds. These
are explicit preconditions, not reasons to erase the settlement loss once the
helper-derived report is accepted.
