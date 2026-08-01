# P4 finding grounding and dispositions: `2025-06-recall-contracts`

All 19 report findings are dispositioned. Only RECL-05 belongs to the selected
Solidity task group and establishes concrete permanent asset loss.

| Report ID | Page(s) | Disposition | Reason |
|---|---:|---|---|
| RECL-01 | 8 | Split out | IPC Rust blob-reader/VM group. |
| RECL-02 | 9-10 | Split out | IPC Rust blob-reader state group. |
| RECL-03 | 11 | Split out | IPC Rust bucket actor group. |
| RECL-04 | 12 | Split out | IPC Rust blobs actor group. |
| RECL-05 | 13 | Include rewarder component as H-01 | Silent successful no-op lets the outer claim processor consume a validator claim without minting or transferring its reward. The gater component is excluded because the report establishes no concrete asset-loss path for it. |
| RECL-06 | 14 | Split out | IPC Rust timehub actor group. |
| RECL-07 | 15 | Split out | IPC Rust blobs state group. |
| RECL-08 | 16 | Split out | IPC Rust blobs actor group. |
| RECL-09 | 17-18 | Split out | IPC Rust actor authentication group. |
| RECL-10 | 19 | Split out | IPC Rust RecallConfig group. |
| RECL-11 | 20-21 | Split out | IPC Rust blobs state group. |
| RECL-12 | 22 | Split out | IPC Rust blob-reader group. |
| RECL-13 | 23 | Exclude | Informational implementation-initializer hardening; no concrete asset-loss sequence. |
| RECL-14 | 24 | Exclude | Atomic faucet recipient compatibility failure; no asset consumed or misdirected. |
| RECL-15 | 25 | Exclude | Event semantics only. |
| RECL-16 | 26 | Exclude | Administrative role-separation recommendation; no concrete asset-loss path. |
| RECL-17 | 27-28 | Exclude | Explicit non-security miscellany; mixed Rust items also belong to IPC. |
| RECL-18 | 29-30 | Split out | IPC Rust syscall group. |
| RECL-19 | 31 | Split out | IPC Rust IPLD hashing group. |

H-01 is limited to `ValidatorRewarder`. The report groups a similar
`ValidatorGater` modifier under RECL-05, but that power-range bypass is not
included in this detect task because it lacks a report-grounded asset-loss
sequence.
