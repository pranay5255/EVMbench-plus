# EigenLayer EigenDA pre-candidate gate failure

Result: **fail closed at finding selection; no EVMBench candidate was created**.

The immutable source, PDF, exact vulnerable Git snapshot, report scope, mixed
Go/Foundry framework, and source baseline all validate. The remaining required
invariant fails: the report and exact code support zero concrete
loss-of-assets findings under the detect-only contract.

## Passed evidence gates

- The immutable OCR JSONL has 33 ordered records covering exactly pages 1–33.
  All 19 global and 1,716 per-record checks passed, with no failed check. Its
  before/after SHA-256 is
  `b6e57d6e6cf6a894a6f9d015170621861b3bc82091e0579efdf7cfa4d41b7686`.
- The source PDF is readable, unencrypted, has 33 physical pages, and matches
  the OCR-recorded SHA-256
  `2900c32ac36fb78949c11cc620c68efe453b411d021a2f09665c91dcb00b42fb`.
  All pages and all 16 finding boundaries were reconciled side by side;
  physical pages 4, 7, 17, and 26 were also rendered and visually inspected.
- The report's repository and short vulnerable SHA resolve exactly to public
  repository `https://github.com/Layr-Labs/eigenda.git`, detached commit
  `066f8ef4f93bb8ce196555904e89adf7ef50e57f`, and root tree
  `c3d52e52d6471ead466775bc80b40b35c62a4f08`. The separate fixed SHA resolves
  to `794c356269b2e9559b6d43e4b21dee7c45eb354b` and was not used as the base.
- All strict scope roots exist at the vulnerable commit. The excluded legacy
  subtree and third-party dependencies remain excluded. The report's two
  out-of-scope asset references (part of EDA-06 and all of EDA-14) are recorded
  without broadening the scope.
- The exact checkout's Go packages compiled, focused Go package tests passed,
  Foundry compiled 216 files with solc 0.8.12, and 23 focused Solidity tests
  passed. The broader Go runtime attempt remains explicitly incomplete because
  some tests require writable SRS resources or a nested Docker daemon.

## Failed required invariant: no eligible detect finding

The report records one Medium, seven Low, and eight Informational findings;
there are no Critical or High findings. Severity alone was not used as the
filter. Each of all 16 items was inspected in the exact vulnerable code for a
concrete attacker sequence and direct or indirect loss of user or protocol
assets.

EDA-02 through EDA-07, EDA-10, and EDA-15 concern cancellation, resource
exhaustion, panics, denial of service, or retry/failover. The report does not
show a permanent asset lock. EDA-01 and EDA-08 are response/input correctness.
EDA-09 still maps a failed certificate check to a non-success status. EDA-11
describes potential downcast truncation but supplies no certificate that
bypasses Merkle and security-parameter checks, much less an asset-loss path.
EDA-12 is logging hygiene. EDA-13 is an explicitly enabled backend-toggle API
that accepts only predefined backends; no asset authority or transfer
destination is exposed. EDA-14 is an out-of-scope limit mismatch that fails at
the lower on-chain constraint. EDA-16 is diagnostic, documentation, and style
cleanup expressly described as having no direct security implications.

`p4-finding-dispositions.md` gives the item-by-item PDF pages, exact code
anchors, and exclusion reasoning. Promoting availability or hardening defects
to an asset-loss gold answer would invent impact not established by the source.
A zero-finding task is also invalid. The failure code is
`NO_ELIGIBLE_ASSET_LOSS_FINDINGS`.

## Prohibited downstream state

- Candidate ID: none.
- Review-bundle digest: none. The digest in this report directory is only a
  pre-candidate gate-evidence digest and cannot be approved for admission.
- Selected findings, gold audit, and OCR gold slices: none.
- Candidate materialization, structural validator, candidate semantic
  validator, candidate source-build validator, and leakage scan: not run.
- The exact repository contains tracked audit PDFs, including one under the
  nominal proxy scope. Because no candidate was created, none entered a task;
  any future candidate packaging would have to exclude them explicitly.
- Canonical EVMBench admission, verifier/agent images, Harbor task generation,
  Harbor replay, and model smoke: not attempted.
- Dirty canonical `forestOfAudits` checkout: inspected read-only and untouched.
- Selected-20 queue: EigenLayer rank 13 is recorded as blocked; Benqi
  Governance remains next. The stale instruction to mark Benqi created and
  Burve next was not applied because Burve is already created and no EigenLayer
  approval exists.

To reopen candidate creation, provide new, independently reviewable evidence
that identifies at least one distinct concrete asset-loss exploit in this
exact commit and strict report scope. It must survive PDF/code grounding and
human review; an availability-only reinterpretation or scope expansion is not
sufficient.
