# C1 review checkpoint: `2025-02-train-protocol`

Status: ready for exact digest-bound human approval; not admitted.

Review-manifest SHA-256:

`4cec4cef2a1fb71efaaf18b811a1a366460edc311b0dd9342517da15d4d3cb65`

## Reviewed identity

- OCR:
  `62d277d7e89186abb4768f98f3da16b501bbd54e67b1940947a97c8bd9bab35e`
- PDF:
  `e064e1c503ded4c074c2b8cde2095ecebcd5f68fe17ea0cfa9b101cc8d2dbe71`
- Repository HEAD:
  `6c96f61d7d6c7e8a8991a12e40068ab53b0a9e7b`
- Candidate checksum stream:
  `1ce649fc112acbeb42ea5f205bca155de8677e49b205811e08827ed18b66d6ad`
- Base image:
  `docker.io/pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0`
- Local review image config:
  `sha256:64a4ff7656582511090e05492a5c0e862ebd03cd8817c6c960bd614a4b6e3e63`

## Finding map

| Candidate | Report | Pages |
|---|---|---:|
| H-01 | LYSWP2-7 | 10–11 |
| H-02 | LYSWP2-6 | 12–13 |
| H-03 | LYSWP2-8 | 14–16 |
| H-04 | LYSWP2-5 | 17–18 |

All nine report findings have dispositions: four included and five excluded.

## Validation

- OCR: 30 ordered records; 19 global and 1,560 record checks passed.
- PDF: exact checksum and 30-page count passed.
- Repository: exact detached commit, three audited files, no submodules.
- Structural validator from clean OPD_base revision
  `38957485d5cd63dc5d664c3c2993f60b308f5776`: passed with no errors or
  warnings; validator tests: 6 passed.
- Hardhat: 30 Solidity files compiled.
- Agent image: built and checked offline at the exact vulnerable HEAD.
- Final image filesystem and build-context leakage checks: passed.
- Canonical EVMBench and Harbor state: unchanged.

## Review disclosures

- Strict `npm ci` hits an upstream Hardhat peer-dependency conflict;
  `npm ci --legacy-peer-deps` reproduces the compile.
- The repository tests fail in setup because they request obsolete artifact
  names; no test body executes.
- Scarb was unavailable, so the byte-verified and code-reviewed Cairo source
  was not compiled.
- H-04 requires a live hard fork with duplicated HTLC state and signature
  replay onto the unintended branch.
- The review image remains local-only. Registry publication, admission, Harbor
  generation, and any agent/model run are post-approval operations.

## Required approval text

`I approve candidate 2025-02-train-protocol at review-bundle digest 4cec4cef2a1fb71efaaf18b811a1a366460edc311b0dd9342517da15d4d3cb65 for admission. Reviewer: https://github.com/pranay5255.`

Until exact approval is supplied, `review_status.yaml` remains `in_review`;
the candidate is not copied into canonical EVMBench, no image is published, no
Harbor task is generated, and no agent/model run is launched.
