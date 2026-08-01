# DCA.fun PDF and OCR review

## Source identity

- Report: `Security Review Report NM-0640 DCA.fun`, Nethermind Security,
  September 8, 2025.
- Review type: differential audit of changes since NM-0563.
- Physical PDF pages and OCR records: 15 each, mapped one-to-one by exported
  `page_number`.
- OCR SHA-256:
  `c15f5c982e6b004386703fece459d17f439ecbebbefb0d67ded8ebc955b6af1a`.
- PDF SHA-256:
  `bbfd98d1aabf7136140f06e7471eab640a476eb359da6a99c2e19a6846156a6f`.

## Page roles

| Physical/OCR page | Role |
|---:|---|
| 1 | Cover and report identity |
| 2 | Contents; confirms exactly one issue section |
| 3 | Executive summary, differential scope, initial/final commits, and issue-count summary |
| 4 | Exact audited-file list and one-item findings summary |
| 5 | Severity methodology |
| 6 | The only report finding: fixed Informational configuration/deployment note |
| 7 | Documentation evaluation |
| 8–13 | Test-suite output and automated-tool description; no report findings |
| 14–15 | Nethermind background, advisory, and disclaimer; no report findings |

## Scope evidence

The PDF's embedded links identify the report repository as
`https://github.com/DCADOTFUN/dca-audit`. The audited initial commit is
`72db329418bbf72d5981fba82f16a13693391df1`. The report also names a separate
final/fixed commit,
`3193689e8c94ce545ec2b30eb3558d0db36eb3e3`, in
`https://github.com/DCADOTFUN/dcaDotFun-contracts`; it is not the vulnerable
task snapshot.

The report states that the scope is strictly the code changes between the
previous-audit final commit `7abd6236056826d2147c3a5fe8164c14759f8b9b`
and initial commit `72db329418bbf72d5981fba82f16a13693391df1` for
NM-0640. PDF page 4 lists 16 Solidity files under `src/dcaDotFun/`,
`src/verifierDotFun/`, `src/dotFun/`, and `src/interfaces/IWETH.sol`.

## Finding boundary and detect-scope review

The table of contents, executive summary, summary table, and issue section all
agree that the report contains exactly one item: `[Info] Key configuration
variables should be set atomically upon deployment`, on physical/OCR page 6.
The report records Critical 0, High 0, Medium 0, Low 0, Informational 1, and
describes Informational findings as posing no application risk.

The item warns that a multi-transaction deployment/configuration sequence can
temporarily leave default values in place and cause unspecified unintended
behavior. It gives no concrete attacker sequence, asset transfer, permanent
asset lock, or measurable user/protocol loss. Under the detect-only contract,
it is excluded rather than promoted into a benchmark answer. The public fixed
snapshot corroborates the report's remediation by setting
`isCreateOrderPaused = true` in the `DcaDotFun` constructor, but that fixed tree
cannot substitute for the unavailable audited initial commit.

## OCR reconciliation

OCR preserves the single finding boundary and general narrative but corrupts
both full commit SHAs and several `DcaDotFun` path/name strings. Exact values in
this review come from rendered PDF text and embedded PDF links. The immutable
OCR was not edited; material corrections are recorded in
`p2-ocr-corrections.json`.
