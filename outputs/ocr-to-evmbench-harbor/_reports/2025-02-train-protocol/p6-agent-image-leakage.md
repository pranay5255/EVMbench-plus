# P6 agent image and leakage validation — Train Protocol

Status: **PASS**

## Image identity

- Local tag: `evmbench-train-protocol:c1`
- Config digest:
  `sha256:64a4ff7656582511090e05492a5c0e862ebd03cd8817c6c960bd614a4b6e3e63`
- Created: `2026-07-27T14:05:24.270997474Z`
- Platform: `linux/amd64`
- Size: `4,188,789,755` bytes
- Published: `no`

## Repository isolation

An offline (`--network none`) container check proved:

- repository HEAD is
  `6c96f61d7d6c7e8a8991a12e40068ab53b0a9e7b`;
- exactly one commit is reachable;
- all three audited files exist;
- no nested Git repositories exist;
- no PDF or JSONL file exists in the agent-visible repository.

## Visibility boundary

The candidate build context is deny-by-default:

```text
**
!Dockerfile
!.dockerignore
```

BuildKit received only the Dockerfile and `.dockerignore`; no finding, gold,
OCR, provenance, review-state, or source-PDF material entered the context.
The fetched repository tree itself contains no tracked PDF or JSONL files.

The final filesystem and tracked-tree scans found none of:

- `findings/`, `gold_audit.md`, finding IDs, or candidate finding titles;
- `ocr_evidence/`, OCR markers, the PDF ID, or the source PDF checksum;
- `provenance.json` or `review_status.yaml`;
- source PDFs or page-level JSONL.

Because host-side evidence was excluded before the build and the exact fetched
Git tree contains none of it, there is no deleted host-evidence layer hidden
below the final filesystem.

## Structural validation

Both the clean pinned OPD_base validator at
`38957485d5cd63dc5d664c3c2993f60b308f5776` and the current validator pass
with zero errors and zero warnings. This is structural/leakage validation, not
human semantic approval.
