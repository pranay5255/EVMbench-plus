# C1 review checkpoint: `2025-01-brava-contracts`

Status: ready for exact digest-bound human approval; not admitted.

Review-manifest SHA-256:

`617de0007ff0087caa3fa062c40f2f2b3c6f49e558d27b6f9893eac74db25167`

## Reviewed identity

- OCR: `359b5683f6e7eedcda602ebf40cd4d7fa2c08811d3fb50e33380ec3a8470e26c`
- PDF: `0a2e01d42de45845dbc5b3aea01cb37458e23a59b256696949f5f4d4f772967d`
- Repository HEAD: `655613454d3c6264096457adeb387b965fefc3c6`
- Root tree: `adc6756be8d1c213aa1ed0e40532654932776d6d`
- Candidate checksum stream: `0ac944543ad96a610840dab71d4b3eade876a59c8af9c190a0a19ea455e99bd8`
- Base image: `docker.io/pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0`
- Local review image config: `sha256:b395ead9583a83c1a8fd430fd75767d0177fadb5afc4cc8e462b27ffba0546d4`
- Local review image tar: `be685b230f6d0ee908d60121340e62b58cd89fa5f0fcdc32c6546e66827ad276`

## Finding map

| Candidate | Report | Severity | Pages | Title |
|---|---|---|---:|---|
| H-01 | BRAV-02 + BRAV-04 + BRAV-05#3 | High/High/Medium | 9, 11-12 | Unguarded Safe control lets owners erase and bypass accrued fees |
| H-02 | BRAV-05#1 | Medium | 12 | Unrestricted exit entry points withdraw positions without charging fees |
| H-03 | BRAV-05#2 | Medium | 12 | SendToken exports fee-bearing position tokens before fees are settled |

All 16 report findings have dispositions. Three concrete fee-loss mechanisms
are selected as gold findings.

## Validation

- OCR: 28 ordered records passed 19 global and 1,456 record-level checks.
- PDF: exact checksum, readability, and 28-page count passed; relevant pages
  were visually compared with OCR.
- Repository: exact detached commit, trees, 37-file audited scope, and no
  submodules passed.
- Structural validators: current and clean pinned OPD revision
  `38957485d5cd63dc5d664c3c2993f60b308f5776` passed with zero errors or
  warnings.
- Validator tests: 9 current tests and 6 pinned candidate-validator tests
  passed.
- Hardhat: the explicit no-cache image build and fresh 92-file force compile
  with runtime networking disabled passed and left Git clean.
- Image: exact vulnerable HEAD, one reachable commit, no remote, no
  unreachable or fixed-commit objects.
- Leakage: 70-byte deny-by-default build context, image history, candidate
  layer, saved archive, runtime filesystem, and Git history passed; zero PDF or
  JSONL files and zero distinctive answer markers were found.
- Canonical `forestOfAudits`, EVMBench, and Harbor state are unchanged. The
  queue ledger records Brava as `in review`; Benqi remains next because Brava
  was explicitly selected out of order.

## Review disclosures

- H-01 merges BRAV-02, BRAV-04, and one BRAV-05 mechanism at the shared
  missing-Safe-guard boundary. BRAV-05's independently reachable exit and
  receipt-token-transfer mechanisms become H-02 and H-03. Human confirmation
  of this grouping is required.
- The unmodified suite requires a Tenderly mainnet fork. With networking
  disabled, zero tests execute and all 18 suites fail in `before all`; no green
  upstream semantic test baseline is claimed.
- `npm audit` reports 76 vulnerabilities in the preserved lockfile dependency
  graph: 12 low, 14 moderate, 42 high, and 8 critical.
- The reviewed image exists only locally. It has not been published, the
  candidate has not been admitted, no Harbor task exists, and no agent/model
  run was launched.

## Exact approval required

Approval must name both the candidate and this digest, and must include the
reviewer's identity:

`I approve candidate 2025-01-brava-contracts at review-bundle digest 617de0007ff0087caa3fa062c40f2f2b3c6f49e558d27b6f9893eac74db25167 for admission. Reviewer: <identity>.`

Any candidate or manifest byte change invalidates this approval request.
