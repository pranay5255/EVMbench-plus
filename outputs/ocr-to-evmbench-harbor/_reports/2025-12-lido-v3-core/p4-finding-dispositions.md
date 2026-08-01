# P4 finding dispositions — Lido v3

Status: **PASS**

The report contains 19 findings. Five distinct, code-grounded asset-loss
findings are included. Fourteen findings are excluded without merging or
silently dropping them.

| Report ID | Severity | Candidate | Disposition |
|---|---:|---:|---|
| H-1 | High | H-01 | Included: known bad debt precedes bunker exit restrictions and shifts loss to remaining holders. |
| M-1 | Medium | H-02 | Included: coupled share-rate effects overstate the socialized loss. |
| M-2 | Medium | H-03 | Included: validator churn weakens the CL growth check; downstream asset loss is labeled as an inference. |
| M-3 | Medium | H-04 | Included: vault operations can add uncapped slashing-derived debt in bunker mode. |
| M-4 | Medium | — | Excluded: invariant/operational safety issue with no distinct verified asset-loss path. |
| M-5 | Medium | H-05 | Included: missing pending debt in smoothing can cause an avoidable negative rebase. |
| L-1 | Low | — | Excluded: parameter front-run without an independent asset-loss path. |
| L-2 | Low | — | Excluded: defense in depth against a hypothetical upstream Accounting bug. |
| L-3 | Low | — | Excluded: comment only. |
| L-4 | Low | — | Excluded: equivalent accessor behavior; maintainability only. |
| L-5 | Low | — | Excluded: infeasible `uint128` share bound with no realistic loss condition. |
| L-6 | Low | — | Excluded: repeated updates remain accounted; integration/gas concern only. |
| L-7 | Low | — | Excluded: safety-check calibration with no concrete asset-loss sequence. |
| L-8 | Low | — | Excluded: admin-input downcast can disable a group, but no verified loss path. |
| L-9 | Low | — | Excluded: visibility/gas style only. |
| L-10 | Low | — | Excluded: arithmetic grouping/readability only. |
| L-11 | Low | — | Excluded: report explicitly states no practical impact. |
| L-12 | Low | — | Excluded: comment only. |
| L-13 | Low | — | Excluded: temporary EL-reward under-distribution without negative rebase or asset destruction. |

The structured, full-length ledger is in the candidate's `provenance.json`.
