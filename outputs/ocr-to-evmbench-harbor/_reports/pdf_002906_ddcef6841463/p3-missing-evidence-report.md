# UFarm pre-candidate gate failure

Result: **fail closed at Gate 3; no EVMBench candidate was created**.

## Passed evidence gates

- The immutable OCR JSONL has 31 ordered records covering exactly pages 1–31.
  All 1,351 global and per-record checks passed, and its before/after SHA-256 is
  `097be42f6831d661eb05870845f9b67b31d75051af4982aa488bd41edfe482fe`.
- The original PDF is present, has 31 physical pages, and matches the recorded
  SHA-256
  `f83b7a21de368b71f90138371290b2f435f72888f840b274649f793e4cb4e281`.
- All scope and finding boundaries were reviewed against rendered PDF pages.
  The PDF's embedded links establish the intended vulnerable commit
  `aa69668de34c7bcd32cb271d082a4398d127b145` and separate fixed commit
  `2fc58b7b810b82a2385ea8e275665311e3b8364f`.
- The fixed public GitHub repository is a Hardhat Solidity project, but this is
  only framework corroboration and not vulnerable-snapshot evidence.

## Failed required invariant

**The exact audited source snapshot is unavailable.** The report links the
vulnerable tree in the MobileUp GitLab project. That GitLab project is not
publicly readable from this environment: Git requires credentials, its API
returns `404 Project Not Found`, and the web endpoint redirects to sign-in. The
audited SHA is absent from the report-linked public GitHub fixed repository,
cannot be fetched directly (`upload-pack: not our ref`), is absent from that
repository's public forks, and has zero matches in GitHub's global commit
index. No archival capture or local copy was found.

The public GitHub parent of the fixed release is not a substitute. It has no
`depositQueue` implementation, while the fixed release adds the Quex queue
feature and its audit remediations together in a 71-file release commit. Thus
neither the parent nor the fixed tree is the audited vulnerable tree, and the
report does not provide a tree hash or patch from which that tree can be
reconstructed exactly.

A second discovery pass checked additional content-addressed sources. Both
historical GitLab registry namespaces reject the CI-derived `aa69668d` image
tag, Software Heritage has neither the origin nor revision, all eight public
GitHub forks return `404` for the commit object, GitHub's global commit search
returns zero matches, and Wayback, Common Crawl, Sourcegraph, public package
registries, local Git bundles, and local Docker images contain no independent
copy. `p3-discovery-refresh.json` records each probe without recording or
exposing credentials.

Without a detached checkout whose `HEAD` is exactly the audited commit, the
workflow cannot verify paths, snippets, root causes, framework behavior, or an
agent image. Choosing a nearby public commit would silently change the task.

## Prohibited downstream state

- Candidate ID: none.
- Review-bundle digest: none; the digest in this directory is a pre-candidate
  gate-evidence digest and cannot be approved for admission.
- Selected findings: none; finding assessments remain provisional and
  ungrounded in audited code.
- Structural, semantic, source-build, and leakage validation: not run because
  no candidate or audited checkout exists.
- Canonical EVMBench admission, images, Harbor generation/replay, and model
  smoke: not attempted.
- Dirty canonical `forestOfAudits` checkout: inspected read-only and untouched.
- Canonical selected-20 queue: untouched; Ufarm remains queued.

The gate can be resumed only with an authenticated fetch of the exact GitLab
commit or a content-addressed Git bundle/archive that proves that commit and
its complete tree. A source ZIP without Git object identity is insufficient.
