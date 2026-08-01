# P2 PDF and OCR review — Lido v3

Status: **PASS**

## Immutable inputs

- PDF:
  `/home/experiments_base/smart-contract-data/crawlers/output/repos/audit_repos/audits_public/Lido/Lido v3/Lido v3 Security Audit Report.pdf`
- PDF SHA-256:
  `394412f5537fe8936dad4362cad9a71bf8d37c4bf7e759bdd2d021e4f98cbcda`
- PDF size: `2,409,580` bytes
- Physical pages: `35`
- Encrypted: `no`
- OCR:
  `/home/experiments_base/OPD_base/outputs/evmbench_task_batch/extracted_pages/pdf_003436_1e68fc3994b5.jsonl`
- OCR SHA-256:
  `f7a5cf35d01708e04abd62a670cad8f66d00025db572ffc15f81d860b0f3fe68`
- OCR size: `215,874` bytes
- OCR records: `35`

The OCR validator passed all 19 global checks and all 1,820 record checks.
Pages are exactly 1–35 and the source JSONL hash was unchanged before and
after validation.

## Report identity

- Title: Lido v3 Security Audit Report
- Report date: December 12, 2025
- Audit period: June 17, 2025 through December 11, 2025
- Initial audited commit:
  `22cab0f0372015f2d2fce8bede64e98beae28571`
- Final audited/deployed-bytecode commit:
  `b98371488eb9479cf072bd6c2b682a59c5dd71d8`
- Findings: 0 Critical, 1 High, 5 Medium, 13 Low

## Scope correction

The page-5 visible text prints:

- `contracts/0.4.24/Lido.sol`
- `contracts/0.8.25/Accounting.sol`

The second embedded PDF annotation links to:

`https://github.com/lidofinance/core/blob/22cab0f0372015f2d2fce8bede64e98beae28571/contracts/0.8.9/Accounting.sol`

At the initial commit, `contracts/0.8.9/Accounting.sol` exists and
`contracts/0.8.25/Accounting.sol` does not. The task therefore records
`contracts/0.8.9/Accounting.sol` as the corrected audited path and preserves
the printed typo in provenance.

## Page map

| Pages | Role |
|---|---|
| 1 | Report identity |
| 2–3 | Contents |
| 4 | Introduction |
| 5 | Repository scope |
| 6 | Initial, re-audit, and final commits |
| 7–8 | Deployments |
| 9–10 | Methodology and risk classification |
| 11–13 | Finding summary |
| 14 | H-1 |
| 15–17 | M-1 |
| 18 | M-2 |
| 19 | M-3 |
| 20 | M-4 |
| 21 | M-5 |
| 22–34 | L-1 through L-13 |
| 35 | Auditor information |

## Material OCR corrections

- Page 6: use visually reviewed PDF annotations for commit hashes; OCR
  confuses hexadecimal `1` and `l`.
- Page 16: use PDF/code numeric separators and values in the M-1 example.
- Page 20: the PDF/code say `stETH` and `require(!isStopped())`.
- Page 21: the PDF/code say `smoothenTokenRebase`, `stETH`, and `elRewards`.

The PDF and pinned repository, not corrupted OCR tokens, control gold wording.
