# C1 review checkpoint: `2025-01-burve`

Status: ready for exact digest-bound human approval; not admitted.

Review-manifest SHA-256:

`c2b30aa4cccf46b249c4dbe935068da942da042ef60419f1800bd72ca5ad903f`

## Reviewed identity

- OCR: `a6ede0f0946928351257c3b0800f75118d716d49438a99aaa287877782b6657a`
- PDF: `9331ef94ce1ae3fecce225d5aa49a08583a66e625fd728463af4ca15b7135404`
- Repository HEAD: `f0597768fee2d00c17429941f4721475e1ca5723`
- Root tree: `77fcc19230827f270cd36d9fbd7df947ec3749be`
- Candidate checksum stream: `4a8e52d71065f4afdd917a9c6a2591a12bb46a2e777e587b777d17dac539269c`
- Base image: `docker.io/pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0`
- Local review image config: `sha256:85cb927dd1831277a5fe6b2f15917bb64796b3a91ec63f1877a34a5b2197c674`
- Local review image tar: `ec20de36a4ee321b6e6e77ad2c50929aef75528f3650d2499a432dedd91bb99a`

## Finding map

| Candidate | Report | Severity | Pages | Title |
|---|---|---|---:|---|
| H-01 | C-01 | Critical | 10 | Broken implied-price arithmetic corrupts swaps and liquidity valuation |
| H-02 | C-02 | Critical | 11–12 | Liquidity additions include the deposit in pool value and under-mint shares |
| H-03 | C-03 | Critical | 13–14 | Unrestricted diamond cuts let any caller replace protocol logic |
| H-04 | C-04 | Critical | 15 | Unrestricted mint callback spends arbitrary users' token approvals |
| H-05 | M-01 | Medium | 19 | Mint and burn lack price bounds and expose users to adverse execution |

All 20 report findings have dispositions: five included and 15 excluded.

## Validation

- OCR: 28 ordered records passed the immutable-input validator.
- PDF: exact checksum, readability, and 28-page count passed.
- Repository: exact detached commit, root tree, 19-file audited scope, and 16 pinned recursive submodule revisions passed.
- Structural validator from clean OPD_base revision `38957485d5cd63dc5d664c3c2993f60b308f5776`: passed with no errors or warnings.
- Validator tests: 9 current tests passed; 6 pinned candidate-validator tests passed.
- Foundry: the no-cache build and a fresh 109-file force rebuild with runtime network disabled passed.
- Agent image: exact vulnerable HEAD, one reachable commit, clean worktree, and no known post-audit commit objects.
- Leakage checks: build context, image layer, saved image archive, runtime filesystem, and Git history passed; zero PDF or JSONL files are agent-visible.
- Canonical `forestOfAudits`, EVMBench, and Harbor state: unchanged; the selected-20 queue ledger now records Burve as `in review`.

## Review disclosures

- The unmodified upstream Foundry suite is not green: 11 tests pass and 16 fail across 27 tests. Failures include setup reverts, cheatcode call-depth expectation mismatches, and one log mismatch. This is the vulnerable baseline, not candidate semantic validation; no finding-specific tests were added.
- The reviewed image vendors the exact pinned dependency sources, strips nested Git metadata and the parent submodule object store, and disables automatic dependency reinstall. The audited source contract files remain exact, and an offline force rebuild passes.
- The reviewed image remains local-only. Registry publication, admission, Harbor generation, and any agent/model run are post-approval operations.

## Required approval text

`I approve candidate 2025-01-burve at review-bundle digest c2b30aa4cccf46b249c4dbe935068da942da042ef60419f1800bd72ca5ad903f for admission. Reviewer: https://github.com/pranay5255.`

Until exact approval is supplied, `review_status.yaml` remains `in_review`; the candidate is not copied into canonical EVMBench, no image is published, no Harbor task is generated, and no agent/model run is launched.
