# DCA.fun pre-candidate gate failure

Result: **fail closed before candidate creation**.

Two independent required invariants fail: the exact audited vulnerable Git
snapshot is unavailable, and the report has no concrete asset-loss finding
eligible for a detect-only task.

## Passed evidence gates

- The immutable OCR JSONL has 15 ordered records covering exactly pages 1–15.
  All 799 global and per-record checks passed, and its before/after SHA-256 is
  `c15f5c982e6b004386703fece459d17f439ecbebbefb0d67ded8ebc955b6af1a`.
- The original PDF is present, readable, has 15 physical pages, and matches the
  recorded SHA-256
  `bbfd98d1aabf7136140f06e7471eab640a476eb359da6a99c2e19a6846156a6f`.
- The report identity, differential scope, full commit identifiers, audited
  file list, issue summary, and only finding were reviewed against rendered PDF
  pages. Exact links and identifiers came from the PDF, not corrupted OCR.
- The PDF establishes the intended report repository
  `https://github.com/DCADOTFUN/dca-audit`, audited initial commit
  `72db329418bbf72d5981fba82f16a13693391df1`, previous-audit final commit
  `7abd6236056826d2147c3a5fe8164c14759f8b9b`, and separate fixed commit
  `3193689e8c94ce545ec2b30eb3558d0db36eb3e3`.

## Failed invariant 1: exact audited snapshot unavailable

The report-linked `DCADOTFUN/dca-audit` repository returns GitHub `404`, and
Git cannot list or fetch it. The full audited SHA has no GitHub commit-search or
web-search match, and GitHub codeload and raw-content endpoints return `404`.
Software Heritage has neither the origin nor the revision. No matching local
checkout, archive, or Docker image was found.

The official public `DCADOTFUN/dcaDotFun-contracts` repository cannot replace
the missing tree. It contains exactly one root commit: the report's separate
final/fixed commit `3193689e8c94ce545ec2b30eb3558d0db36eb3e3`. That repository
does not contain the audited `72db329418bbf72d5981fba82f16a13693391df1`
object and has no public forks. Its constructor includes the reported fix,
`isCreateOrderPaused = true`, proving it is remediation corroboration rather
than the vulnerable snapshot.

Without a detached checkout whose `HEAD` is exactly the audited commit, the
workflow cannot validate the differential scope, vulnerable implementation,
or source build. Selecting the fixed one-commit repository would silently
change the task.

## Failed invariant 2: no eligible detect finding

The report contains exactly one item and records Critical 0, High 0, Medium 0,
Low 0, and Informational 1. Its own methodology says Informational findings do
not pose application risk. The item warns generally that deployment through
multiple setter transactions can temporarily leave default values and cause
unspecified unintended behavior. It does not establish an attacker-controlled
sequence, asset transfer, permanent asset lock, or concrete loss to a user or
the protocol.

The workflow forbids inventing a stronger impact than the verified report and
code establish. Consequently the only item is excluded, leaving zero selected
findings and no valid detect task even if the missing snapshot later becomes
available without additional qualifying evidence.

## Prohibited downstream state

- Candidate ID: none.
- Review-bundle digest: none. The digest in this report directory is a
  pre-candidate gate-evidence digest and cannot be approved for admission.
- Selected findings and gold audit: none.
- Structural, semantic, source-build, Docker, and leakage validation: not run
  because no valid candidate or vulnerable checkout exists.
- Canonical EVMBench admission, images, Harbor generation/replay, and model
  smoke: not attempted.
- Dirty canonical `forestOfAudits` checkout: inspected read-only and untouched.
- Canonical selected-20 queue: DCA is recorded as blocked; Benqi Governance
  remains next, and the stale post-approval instruction was not applied.

To resume repository verification, provide a content-addressed Git bundle or
public origin that proves the complete object
`72db329418bbf72d5981fba82f16a13693391df1`. To create a detect candidate,
there must also be verified evidence of at least one distinct concrete
asset-loss vulnerability in that exact differential scope; the current report
does not supply one.
