# P4 finding dispositions — Hemi Labs VUSD

Status: **PASS**

Three of the report's ten bugs have distinct code-grounded direct or indirect
asset-loss paths in the exact vulnerable snapshot.

| Report ID | Pages | Severity | Retest status | Disposition | Candidate |
|---|---:|---|---|---|---|
| Bug ID #1 | 16 | High | Acknowledged | Included: a zero or unsafe caller-controlled output floor lets a sandwich extract Treasury COMP rewards. | H-01 |
| Bug ID #2 | 17 | Medium | Fixed | Included: issuance uses nominal input before a fee-on-transfer deposit, creating undercollateralized VUSD. | H-02 |
| Bug ID #3 | 18 | Medium | Acknowledged | Included: `deadline = block.timestamp` is always current and permits adversarially delayed execution within the output floor. | H-03 |
| Bug ID #4 | 19–20 | Medium | Acknowledged | Excluded: the exact code already bounds stablecoin oracle answers to a governor-configured 1% tolerance; the report does not prove a circuit-breaker bound inside that range or another concrete loss path. | — |
| Bug ID #5 | 21–22 | Low | Partially fixed | Excluded: missing monitoring events do not create an on-chain asset-loss path. | — |
| Bug ID #6 | 23–24 | Low | Acknowledged | Excluded: generic compiler-version advice without a named compiler bug reachable in the snapshot. | — |
| Bug ID #7 | 25–26 | Gas | Acknowledged | Excluded: constant visibility is a gas/readability concern only. | — |
| Bug ID #8 | 27–28 | Gas | Acknowledged | Excluded: inequality micro-optimization only. | — |
| Bug ID #9 | 29 | Gas | Acknowledged | Excluded: increment micro-optimization only. | — |
| Bug ID #10 | 30 | Gas | Acknowledged | Excluded: require-statement micro-optimization only. | — |

## Distinct-root-cause check

- H-01 requires a protocol-side output-floor check.
- H-02 requires received-balance accounting in `Minter._mint`.
- H-03 requires a fixed transaction expiry.

No single repair removes more than one of these root causes. H-01 and H-03
touch the same Treasury swap but constrain different dimensions: acceptable
output and acceptable execution time.

## Review disclosures

- H-01 requires a keeper/governor to submit an unsafe `_minOut`; the external
  attacker then extracts protocol yield through the public route.
- H-02 is conditional on a fee-on-transfer token being whitelisted. The
  vulnerable API is public, and the immediate audit fix confirms the balance
  delta was the intended accounting invariant.
- H-03's maximum direct loss is bounded by `_minOut` when that value is safe;
  its root cause gives block producers indefinite optionality to choose the
  worst still-valid execution point.
