# P2 PDF and OCR review — Train Protocol

Status: **PASS**

## Immutable inputs

- PDF:
  `/home/experiments_base/smart-contract-data/crawlers/output/repos/audit_repos/Smart-Contract-Review-Public-Reports/train_protocol-feb-25(Public)_upd.pdf`
- PDF SHA-256:
  `e064e1c503ded4c074c2b8cde2095ecebcd5f68fe17ea0cfa9b101cc8d2dbe71`
- PDF size: `11,206,973` bytes
- Physical pages: `30`
- Encrypted: `no`
- OCR:
  `/home/experiments_base/OPD_base/outputs/evmbench_task_batch/extracted_pages/pdf_002905_2a0554b0cbcc.jsonl`
- OCR SHA-256:
  `62d277d7e89186abb4768f98f3da16b501bbd54e67b1940947a97c8bd9bab35e`
- OCR size: `150,291` bytes
- OCR records: `30`

The OCR validator passed all 19 global checks and all 1,560 record checks.
Pages are exactly 1–30 and the source JSONL hash was unchanged before and
after validation.

## Report identity

- Title: Security Review Report for Train Protocol
- Auditor: Hexens
- Report month: February 2025
- Audit period: February 3–10, 2025
- Findings: 0 Critical, 1 High, 2 Medium, 2 Low, 4 Informational

## Scope and commits

The page-5 annotations identify the vulnerable repository and commit:

`https://github.com/layerswap/layerswap-atomic-bridge.git`

`6c96f61d7d6c7e8a8991a12e40068ab53b0a9e7b`

Audited files:

- `chains/evm/solidity/contracts/HashedTimeLockERC20.sol`
- `chains/evm/solidity/contracts/HashedTimeLockEther.sol`
- `chains/starknet/src/HashTimeLockedERC20.cairo`

The same page labels two later commits in
`https://github.com/TrainProtocol/contracts.git`:

- `f27f0eaf2b2cc784d5746b0ed9cc42ef88241a5a`
- `ee0391e6f864faea0faecf51b5ffbf16d455fb62`

Those commits are post-audit corroboration only. They do not replace the
page-5 vulnerable repository and snapshot.

## Page map

| Pages | Role |
|---|---|
| 1 | Report identity |
| 2 | Contents |
| 3 | Auditor information |
| 4 | Executive summary |
| 5 | Repository, vulnerable commit, scope, and post-audit commits |
| 6 | Audit dates and reviewer |
| 7–8 | Severity methodology |
| 9 | Finding summary |
| 10–11 | LYSWP2-7 |
| 12–13 | LYSWP2-6 |
| 14–16 | LYSWP2-8 |
| 17–18 | LYSWP2-5 |
| 19–20 | LYSWP2-13 |
| 21–25 | LYSWP2-3 |
| 26 | LYSWP2-10 |
| 27 | LYSWP2-11 |
| 28–29 | LYSWP2-12 |
| 30 | Closing page |

## Material OCR corrections

- Page 5: the embedded annotations supply the full vulnerable commit; OCR
  corrupts the middle of two displayed URLs.
- Pages 10–11: the visually reviewed report ID is `LYSWP2-7`.
- Pages 17–18: the visually reviewed report ID is `LYSWP2-5`.
- Pages 19–20: the visually reviewed report ID is `LYSWP2-13`, not OCR's
  `LYSWP2-i3`.
- Pages 28–29: the visually reviewed report ID is `LYSWP2-12`, not OCR's
  `LYSWP2-i2`.

The PDF annotations and pinned repository, not OCR-corrupted tokens, control
the candidate identity and gold wording.
