# C1R1 human review checkpoint: Mellow Flexible Vaults

Candidate `2025-09-mellow-flexible-vaults` has returned to `in_review`. The
exact approval object is `c1r1-review-manifest.json` (9,479 bytes), SHA-256:

`272a35f142fe209d617296a3366c6f6a42e5b78f213df8792c8e9da9e02c45e1`

## Why C1 was superseded

The C1 review manifest at digest
`7eba708f41fa4d90f56d47e170b8a624aafc84032bade60a88470929d740ee63`
was explicitly approved by `github.com/pranay5255`. Its exact bytes were
admitted only in a disposable isolated checkout at commit
`25d8e83f47ee238a1bb4ecdf1edd76a4de67829b`; nothing was published and no
Harbor or agent/model run started.

Mandatory image construction then exposed two defects in the approved
Dockerfile: an unqualified command selected the base image's Forge 1.3.6
instead of pinned Forge 1.7.1, and deleting all PDFs dirtied recursive
dependencies because some PDFs were tracked there. The corrected Dockerfile
also pins the runtime PATH/compiler and strips nested Git history/remotes while
preserving dependency files as inert clean directories. Because the Dockerfile
bytes changed, the C1 approval cannot carry over.

Only `Dockerfile`, `provenance.json`, and `review_status.yaml` differ from the
approved C1 candidate. The config, H-01 finding, gold answer, both OCR evidence
slices, repository commit/tree/scope, and impact policy remain byte-identical.

## C1R1 validation

The corrected local image is
`sha256:b8353777d6b0188664e6b27cfda3cd3d80f7c3b89d2e4e8ad5adb17b590b2aea`.
It is local only and has no registry digest. With network disabled, it resolves
Forge to `/usr/local/bin/forge` 1.7.1 and solc to the pinned 0.8.25 binary,
contains exact commit `60c462d6...` and tree `6a5951f9...`, has one reachable
commit, no source remote, a clean root, and eight inert nested Git directories
with no HEAD, remote, or objects. It contains no PDF/JSONL, gold, provenance,
review-status, or OCR-evidence artifact. A forced default-command Forge build
also passed with `--network none`.

The live and skill-pinned candidate validators passed, including 6/6 validator
tests in each checkout. The earlier OCR/PDF/snapshot/semantic/build/unit and
byte-exact slice evidence remains bound into the C1R1 review manifest.

## Remaining disclosed risks

- The integration suite requires `ETH_RPC` and was not replayed.
- License metadata is inconsistent: BUSL-1.1 source/README markers, no
  standalone license file, and `UNLICENSED` in `package.json`.
- H-01 requires an authorized helper-derived report to pass threshold
  validation and be accepted.

## Required approval

Admission requires an explicit approval naming:

1. candidate `2025-09-mellow-flexible-vaults`;
2. checkpoint `C1R1` and digest
   `272a35f142fe209d617296a3366c6f6a42e5b78f213df8792c8e9da9e02c45e1`;
3. reviewer identity.

Until then, C1R1 is not admitted, no image is published, no Harbor task is
generated, and no verifier or agent/model run occurs.
