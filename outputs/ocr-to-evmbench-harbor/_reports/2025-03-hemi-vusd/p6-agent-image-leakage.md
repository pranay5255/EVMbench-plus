# P6 agent-image and leakage validation — Hemi Labs VUSD

Status: **PASS**

## Built image

- Local tag: `evmbench-hemi-vusd:c1`
- Image config digest:
  `sha256:6d5805038ba1478c51900f86a7714fa5db7c972da2333fd640b3aedd088c351d`
- Platform: `linux/amd64`
- Size: `4,480,508,923` bytes
- RootFS layers: `20`
- Published: no

The build context allowlists only the `1,316`-byte Dockerfile and
`30`-byte `.dockerignore`. The allowlist is exactly those two files.

## Offline repository check

The image was started with Docker network mode `none`.

- `/home/agent/audit` HEAD:
  `54f9f235f26df813152b3d3235e7f4373ce473b6`
- Reachable commit count: `1`
- Worktree status: clean, including untracked files
- Recursive submodules: none
- Tracked PDF/JSONL paths: none
- Hardhat artifacts for Treasury, Minter, and Redeemer: present

## Full-filesystem boundary scan

The offline scan walked the complete container root except virtual
`/dev`, `/proc`, `/run`, and `/sys` mounts:

- regular files scanned: `164,357`;
- bytes scanned: `4,476,482,419`;
- PDF files: `0`;
- JSONL files under `/home/agent`: `0`;
- forbidden candidate/review/gold filenames: `0`;
- hits for the source PDF/OCR hashes, PDF ID, OCR layout markers, candidate
  finding titles, provenance fields, or evidence paths: `0`.

The immutable base image contains 12 unrelated LiteLLM guardrail benchmark
JSONL fixtures under `/usr/local/lib/python3.12/dist-packages/`. They contain
none of the Hemi PDF, OCR, provenance, or gold markers and are not under the
agent repository. They are disclosed rather than misreported as absent.

No source PDF, Hemi OCR JSONL, authoring provenance, review state, gold finding,
or expected-answer material is visible in the reviewed image.
