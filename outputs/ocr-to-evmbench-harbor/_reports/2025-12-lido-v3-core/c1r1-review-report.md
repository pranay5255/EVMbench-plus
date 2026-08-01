# C1R1 review checkpoint: `2025-12-lido-v3-core`

Status: ready for exact digest-bound human approval; not admitted.

Review-manifest SHA-256:

`8e276720b26afb8c760a8bb3a8dc791a47c5f2ff1f023b4ceddcbd0777a0e663`

Reviewer identity verified with `gh api`:

`https://github.com/pranay5255`

## Reviewed identity

- OCR:
  `f7a5cf35d01708e04abd62a670cad8f66d00025db572ffc15f81d860b0f3fe68`
- PDF:
  `394412f5537fe8936dad4362cad9a71bf8d37c4bf7e759bdd2d021e4f98cbcda`
- Repository HEAD:
  `22cab0f0372015f2d2fce8bede64e98beae28571`
- Candidate checksum stream:
  `545459a4c40d24ff821aca4bf751c755abf0fd6d90edd5de513d673fc047b7d6`
- Base image:
  `docker.io/pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0`
- Local review agent image config:
  `sha256:5b9ba64cb56749554da391939e53e29ce4d7c1663fa0fa981b144ff4e144e416`

## Finding map

| Candidate | Report | Pages |
|---|---|---:|
| H-01 | H-1 | 14 |
| H-02 | M-1 | 15–17 |
| H-03 | M-2 | 18 |
| H-04 | M-3 | 19 |
| H-05 | M-5 | 21 |

All 19 report findings have dispositions: five included and fourteen excluded.
`gold_audit.md` is verified as the ordered full byte combination of H-01
through H-05.

## Validation

- OCR: 35 ordered records; 19 global and 1,820 record checks passed.
- Structural validator from clean OPD_base revision
  `38957485d5cd63dc5d664c3c2993f60b308f5776`: passed with no errors or
  warnings; validator tests: 6 passed.
- Hardhat: 408 Solidity files compiled; 2,555 tests passed, zero failed,
  19 pending under repository-pinned Node 22.15.0.
- Network-disabled forced compile: passed.
- Final image filesystem and raw agent-added repository layer leakage scans:
  passed.
- Agent-visible repository: clean, one reachable vulnerable commit, no
  post-audit commit objects, PDF, OCR, gold, provenance, or nested Git
  metadata.

## Review disclosures

- The report prints `contracts/0.8.25/Accounting.sol`; its embedded GitHub link
  and the vulnerable tree prove the audited file is
  `contracts/0.8.9/Accounting.sol`.
- H-03's report directly establishes a validator-churn bypass of the annual CL
  balance check. Its holder-loss sequence is explicitly disclosed as a
  code-grounded inference requiring an erroneous or compromised oracle report
  and early exits.
- The review agent image remains local-only. Canonical publication is a
  post-approval operation.

## Required approval text

`I approve candidate 2025-12-lido-v3-core at review-bundle digest 8e276720b26afb8c760a8bb3a8dc791a47c5f2ff1f023b4ceddcbd0777a0e663 for admission. Reviewer: https://github.com/pranay5255.`

Until that exact approval is supplied, `review_status.yaml` remains
`in_review`; the candidate is not copied into canonical EVMBench, no Harbor
task is generated, no canonical image is published, and no agent/model smoke
is run.
