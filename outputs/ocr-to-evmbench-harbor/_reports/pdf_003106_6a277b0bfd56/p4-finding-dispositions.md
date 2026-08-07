# Agora StableSwap finding dispositions before candidate creation

No finding is selected because none can be grounded in the exact audited Git
snapshot. The table still records the complete PDF-level `loss_of_assets`
screen so a later retry does not confuse report plausibility with verified
benchmark gold.

| Report ID | Exported pages | Severity/status | PDF-level loss-of-assets assessment | Pre-candidate disposition |
|---|---:|---|---|---|
| M-01 | 10–11 | Medium, Acknowledged | Inverse-price handling with negative interest produces a materially wrong swap price. Mispricing may enable value extraction, but the report gives no complete attacker sequence and the code is unavailable. | Hold for exact-code review; not selected. |
| L-01 | 12 | Low, Acknowledged | A swap can front-run an admin reserve top-up before `sync()`, allegedly taking deposited tokens without input. | Report-level concrete theft candidate; not selected until exact code and sequencing are verified. |
| L-02 | 12–13 | Low, Resolved | Initialization can revoke the only access-control manager when deployer and initial admin coincide. | Exclude under `loss_of_assets`: administrative lockout without a concrete asset-loss path. |
| L-03 | 13–14 | Low, Resolved | The factory checks the wrong sorted token for zero address. | Exclude: deployment/input-validation failure without a concrete loss sequence. |
| L-04 | 14 | Low, Acknowledged | Standard Uniswap V2 routers cannot discover or price these pools. | Exclude: integration incompatibility only. |
| L-05 | 14–15 | Low, Acknowledged | Fee-on-transfer tokens can revert as input or deliver less output than requested. | Exclude: unsupported-token compatibility/transfer-fee behavior; no distinct attacker-driven drain is established. |
| L-06 | 15 | Low, Acknowledged | Tightening fee bounds does not lower an already configured fee and may overcharge users. | Exclude: privileged configuration inconsistency without a concrete attacker-controlled loss path. |
| L-07 | 15–16 | Low, Acknowledged | A flash-swap callback can allegedly make permissionless `claimFor` rewards look like attacker input, receiving output without supplied input. | Report-level concrete asset-theft candidate; not selected until token assumptions and exact swap code are verified. |
| L-08 | 16–17 | Low, Acknowledged | Linear interest does not model compounding yield and can misprice yield tokens. | Exclude on current evidence: pricing-quality mismatch without a concrete exploit/loss sequence. |
| L-09 | 17–18 | Low, Acknowledged | A trader can sandwich a discrete oracle-price update when the price change exceeds fees. | Report-level concrete arbitrage candidate; not selected until permissions, price bounds, and exact code are verified. |
| L-10 | 18–19 | Low, Resolved | Delayed price-setting transactions use execution time and lack a deadline. | Exclude: stale-transaction correctness risk without a concrete asset-loss sequence. |
| L-11 | 19–20 | Low, Resolved | `getAmountsIn` ignores output-side accumulated fees and can quote a swap that later reverts. | Exclude: quote/revert availability issue only. |
| L-12 | 20–21 | Low, Acknowledged | An alternate token entry-point can allegedly bypass token equality checks and drain balances including accumulated fees. | Report-level concrete fee-drain candidate; not selected until alias-token behavior and privileged caller constraints are verified in exact code. |
| L-13 | 21–24 | Low, Acknowledged | Long negative-rate decay underflows and blocks price-dependent calls. | Exclude: denial of service only under the canonical policy. |
| L-14 | 24–25 | Low, Acknowledged | Fixed/no-slippage pricing can diverge from markets and let arbitrage remove all of the overvalued pool asset. | Report-level concrete protocol-loss candidate; not selected until intended economics and exact implementation are verified. |
| L-15 | 25–29 | Low, Acknowledged | A callback can mutate fee state after a memory snapshot, leaving reserves stale and allegedly enabling a drain. The report PoC grants the callback `TOKEN_REMOVER_ROLE`. | Report-level concrete but threat-model-sensitive candidate; not selected until role reachability, state updates, and drain are reproduced at the exact commit. |

Selected distinct loss-of-assets root causes: **0**.

Report-level retry candidates requiring exact-code verification: **M-01, L-01,
L-07, L-09, L-12, L-14, and L-15**. This list is not a finding set, gold audit,
or approval request.
