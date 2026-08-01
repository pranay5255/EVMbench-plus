# Accountable OCR to EVMBench/Harbor documentation

Status date: `2026-07-27`

Proposed candidate ID: `2025-10-accountable`

Current state: `P1_repository_snapshot_blocked_P2_evidence_complete`

This directory is host-side authoring material. It is not an EVMBench
candidate, an admitted audit, a Docker build context, or a Harbor task. None of
its contents may enter an agent-visible image or generated Harbor directory.

## Gate summary

| Gate | Result | Evidence |
|---|---|---|
| Preserved OCR JSONL | Pass | P2 report: 37 ordered records, pages `1..37`, 19 global plus 1,924 record checks with zero failures, unchanged SHA-256 |
| Original PDF | Pass | P2 report: unchanged SHA-256, 37 physical pages, 33 finding ranges reconciled |
| One repository, vulnerable commit, and audited scope | Blocked | P1 reports: authenticated `gh api` checks with `repo` scope still return `404`; the full account-visible inventory has no matching repository, and no exact commit object was recovered |
| Candidate materialization | Not started | Gate 3 has not passed |
| Human approval | Not applicable | No candidate or review-bundle digest exists |
| EVMBench admission and Harbor execution | Not started | Post-approval work only |

## Documents

1. [01_SOURCE_EVIDENCE_AND_GATE_STATUS.md](01_SOURCE_EVIDENCE_AND_GATE_STATUS.md)
   records immutable inputs, PDF/OCR reconciliation, scope, GitHub API
   discovery, and the exact missing-evidence condition.
2. [02_FINDING_REVIEW_WORKSHEET.md](02_FINDING_REVIEW_WORKSHEET.md)
   accounts for all 33 report findings and records preliminary loss-of-assets
   and deduplication questions. Nothing in this worksheet is approved gold.
3. [03_EVMBENCH_HARBOR_PRD.md](03_EVMBENCH_HARBOR_PRD.md)
   specifies the candidate, visibility boundary, EVMBench package, Harbor
   wrapper, verifier, and acceptance criteria.
4. [04_PHASED_TASK_PLAN.md](04_PHASED_TASK_PLAN.md)
   defines the resumable, approval-gated execution sequence and required
   artifacts.

## Completed host-side evidence reports

The P1 discovery record and completed P2 source-evidence reports are under:

`outputs/ocr-to-evmbench-harbor/_reports/2025-10-accountable/`

P1 produced a fail-closed missing-evidence record. P2 independently passed and
froze the 33-finding page map plus five PDF-grounded OCR corrections. P2 does
not substitute for the missing Git snapshot.

## Exact resume condition

Do not create `outputs/ocr-to-evmbench-harbor/2025-10-accountable/` until an
isolated Git checkout can prove all of the following:

- one canonical repository identity;
- commit `fc43546fe67183235c0725f6214ee2b876b1aac6` exists as a commit object;
- detached `HEAD` equals that commit;
- all required submodules are pinned and initialized;
- every PDF-scoped source file exists in that tree;
- selected findings are verified against that exact vulnerable code.

Acceptable recovery routes include restored authenticated access to the
original repository, an official public mirror containing the same commit
object, or a trusted Git bundle that preserves the commit and its history. A
report excerpt, OCR text, reconstructed source tree, verified deployment, or
post-audit version is not an exact-snapshot substitute.

## Work deliberately not performed

- No source PDF or OCR row was changed.
- No candidate directory or gold finding was created.
- No canonical OPD_base, EVMBench, or Harbor checkout was modified.
- No image was built.
- No Harbor dataset was generated.
- No agent or model was run.
- No human approval was inferred.
