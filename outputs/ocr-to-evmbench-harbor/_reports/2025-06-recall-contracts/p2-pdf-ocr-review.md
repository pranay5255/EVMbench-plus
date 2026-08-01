# P2 PDF and OCR review: Recall Labs

The exact PDF with SHA-256
`f737f649ece8716f7cb4e7f7d6a3df97ca496b12c1bbda0e26c0d0c73a052fc1`
has 33 physical pages, matching all 33 ordered OCR records.

| Exported page | Role | PDF/OCR reconciliation |
|---:|---|---|
| 1 | Identity | Report title, version 2.2, and June 2025 identity agree. |
| 4 | Scope | PDF and OCR both name `recallnet/contracts` at short commit `5a67104`, `recallnet/ipc` at `d08b279`, and an additional `ValidatorRewarder.sol` refactor at `fe4d3b4`. Full commits were resolved from the linked public repositories. |
| 13 | Finding | PDF and OCR agree on RECL-05, High severity/impact, the silent `whenActive` return, the `notifyValidClaim` loss sequence, and PR #57 remediation. |

The only selected finding occupies exported page 13 in full. Page 14 starts
RECL-06, so no adjacent finding page enters H-01. OCR footer/logo corruption
and a missing dot in `ValidatorGater.sol` were corrected only in normalized
review notes; the preserved JSONL remains byte-identical.
