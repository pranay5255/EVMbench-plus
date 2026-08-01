# C1 review checkpoint: `2025-03-hemi-vusd`

Status: ready for exact digest-bound human approval; not admitted.

Review-manifest SHA-256:

`0d7d24df7170e763f532343a98227c3abdf86600036ce94240ca91bc26913c42`

## Reviewed identity

- OCR:
  `a79ba90ae9ed42bf8d7e620bbb06ea36799f13b5f33dcefc36b477614ff21182`
- PDF:
  `76d151f58c3edb5688802c8bd5dbd3727bb3b4a0d3ecc858b4b88e457a8be6e3`
- Repository HEAD:
  `54f9f235f26df813152b3d3235e7f4373ce473b6`
- Candidate checksum stream:
  `9c0f3e33b7c6a4bd2b2808ced003a0bebff485ea24cdd61db6e2a4affa9c2656`
- Base image:
  `docker.io/pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0`
- Local review image config:
  `sha256:6d5805038ba1478c51900f86a7714fa5db7c972da2333fd640b3aedd088c351d`

## Finding map

| Candidate | Report | Pages |
|---|---|---:|
| H-01 | Bug ID #1 | 16 |
| H-02 | Bug ID #2 | 17 |
| H-03 | Bug ID #3 | 18 |

All ten report bugs have dispositions: three included and seven excluded.

## Validation

- OCR: 32 ordered records; 19 global and 1,664 record checks passed.
- PDF: exact checksum and 32-page count passed.
- Repository: exact detached commit, `contracts/` scope, no submodules.
- Structural validator from clean OPD_base revision
  `38957485d5cd63dc5d664c3c2993f60b308f5776`: passed with no errors or
  warnings; validator tests: 6 passed.
- Current structural validator and tests: passed; 6 tests passed.
- Hardhat: 29 Solidity files compiled and 30 artifacts generated.
- Agent image: built and checked offline at the exact vulnerable HEAD.
- Full image filesystem and two-file build-context leakage checks: passed.
- Candidate manifest: 13 files, byte and checksum stream verified.
- Canonical EVMBench and Harbor state: unchanged.

## Review disclosures

- The PDF, not OCR, establishes the commit. OCR inserts one extra `3` in the
  displayed SHA; the visually verified and repository-resolved SHA is
  `54f9f235f26df813152b3d3235e7f4373ce473b6`.
- The locked upstream test runner fails before discovery because its gas
  reporter selects a Mocha reporter that the locked Mocha rejects. The exact
  snapshot still compiles successfully.
- H-01 requires a keeper or governor to submit an unsafe output floor.
- H-02 requires a fee-on-transfer collateral token to be whitelisted.
- H-03 gives indefinite inclusion optionality, but a safe nonzero `_minOut`
  bounds direct loss.
- The review image remains local-only. Registry publication, isolated
  admission, and Harbor generation are post-approval operations.
- The user's final smoke waiver is recorded. After approval, no agent/model
  run will be launched; admission, image publication, Harbor generation,
  loader validation, and verifier packaging still remain required.

## Required approval text

`I approve candidate 2025-03-hemi-vusd at review-bundle digest 0d7d24df7170e763f532343a98227c3abdf86600036ce94240ca91bc26913c42 for admission. Reviewer: <reviewer identity>.`

Until exact approval is supplied, `review_status.yaml` remains `in_review`;
the candidate is not copied into EVMBench, no image is published, no Harbor
task is generated, and no agent/model run is launched.
