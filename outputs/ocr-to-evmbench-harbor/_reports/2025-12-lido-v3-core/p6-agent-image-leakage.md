# P6 agent-image leakage audit — Lido v3

Status: **PASS**

Image:
`evmbench-lido-v3-core:c1`

Image/config digest:
`sha256:5b9ba64cb56749554da391939e53e29ce4d7c1663fa0fa981b144ff4e144e416`

## Repository isolation

- `HEAD` is exactly
  `22cab0f0372015f2d2fce8bede64e98beae28571`.
- `git rev-list --all --count` is exactly `1`.
- The root worktree is clean, including untracked files.
- No nested `.git` file or directory remains.
- Root `.git/modules` is absent.
- The later final commit
  `b98371488eb9479cf072bd6c2b682a59c5dd71d8` is absent.

## Evidence isolation

The audit tree contains no PDF or JSONL file. A byte-oriented recursive scan
also found none of:

- PDF ID or source PDF/OCR hashes
- report title
- `gold_audit.md`
- `provenance.json`
- `ocr_evidence`
- any of the five candidate finding titles

The Docker build context is allowlisted by `.dockerignore` to only
`Dockerfile` and `.dockerignore`; the Dockerfile uses no `COPY` or `ADD`.

The raw agent-added repository layer was also scanned directly, not only the
merged final filesystem. Diff ID
`sha256:c9611a333d2b456bd56cef11f5df6677739251f14ee20acc431860c767db48fd`
contains none of the forbidden filenames or textual markers above, no nested
Git metadata, and no PDF/JSONL file. This closes the deleted-file/renamed-copy
case for material created during the single repository build layer.

## Offline usability

With Docker networking disabled, a forced Hardhat compile succeeded for all
408 Solidity files. The image therefore contains its pinned Yarn dependencies
and Solidity compiler cache without exposing host-side evidence.
