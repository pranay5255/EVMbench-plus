# P4 finding grounding and dispositions: `2025-01-burve`

Status: passed — all 20 report findings are dispositioned, with no unresolved
items.

| Report ID | Physical pages | Disposition | Code-grounded reason |
|---|---:|---|---|
| C-01 | 10 | Include as H-01 | Broken fixed-point reserve division corrupts implied prices used by swaps and liquidity valuation. |
| C-02 | 11–12 | Include as H-02 | The post-deposit balance inflates the share denominator and transfers deposit value to existing LPs. |
| C-03 | 13–14 | Include as H-03 | The installed diamond-cut facet has its admin check commented out, permitting arbitrary delegatecall upgrades and total asset theft. |
| C-04 | 15 | Include as H-04 | Any caller can spend a victim's Burve token allowance into the pool without crediting a position. |
| H-01 | 16 | Exclude | Missing island funding makes mint revert atomically; availability only. |
| H-02 | 16–17 | Exclude | Single-element normalization reverts before state or assets commit; availability only. |
| H-03 | 17–18 | Exclude | Default burn reverts, but the report documents direct and batched recovery paths; no permanent loss. |
| M-01 | 19 | Include as H-05 | No execution bounds let a price move or sandwich settle at fewer shares or tokens than the user intended. |
| M-02 | 20 | Exclude | A paused vault blocks the aggregate withdrawal temporarily; no theft or destruction. |
| M-03 | 21–22 | Exclude | Fee-on-transfer behavior makes the pool mint revert atomically rather than leave an underfunded position. |
| M-04 | 23 | Exclude | Missing initial selectors are recoverable through the upgradeable diamond and do not establish asset loss. |
| M-05 | 24 | Exclude | ERC-165 detection compatibility only. |
| L-01 | 25 | Exclude | Self-allowance is an extra approval and gas cost, not loss of LP or underlying assets. |
| L-02 | 25–26 | Exclude | Zero-approval incompatibility reverts; availability only. |
| L-03 | 26 | Exclude | The report explicitly says the relevant pending-withdrawal state is currently unreachable. |
| L-04 | 26 | Exclude | Non-standard approval return behavior reverts atomically; compatibility only. |
| L-05 | 26–27 | Exclude | Non-string metadata can prevent deployment but cannot lose assets in an existing position. |
| L-06 | 27 | Exclude | Missing token registration validation is present, but the report does not establish a complete reachable asset-loss sequence. |
| L-07 | 27 | Exclude | Only unsolicited ETH can be stranded, and the upgradeable diamond can add recovery; not a normal protocol asset flow. |
| L-08 | 27–28 | Exclude | Strict tick boundaries reject configurations; they do not mis-settle assets. |

The five included findings have independent root causes and direct loss paths.
The report's severity label was not used as an automatic inclusion rule.
