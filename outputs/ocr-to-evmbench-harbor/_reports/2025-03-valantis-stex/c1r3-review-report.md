# C1R3 review checkpoint: `2025-03-valantis-stex`

Status: ready for exact digest-bound human approval; not admitted.

Review-manifest SHA-256:

`11dd3b8f667da20aab1d343e804e7f53122ee64a5b0d086fc27a53445e05fe01`

Reviewer identity verified with `gh api`:

`https://github.com/pranay5255`

Reviewed immutable images:

- Base: `docker.io/pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0`
- Agent: `docker.io/pranay5255/yudaii_evmbench@sha256:a24989c61134ccfed57c61c5a978b1e871fed2c75202039899f267688fc20f44`

The refreshed structural, semantic, repository, no-cache image build, offline Foundry, registry, and full image-layer leakage gates pass. Foundry compiled 102 files and ran 34 passing tests with zero failures or skips. The image contains only the vulnerable commit, has one reachable commit, and exposes no PDF, OCR, gold, provenance, review, or post-audit fix material.

Required approval text:

`I approve candidate 2025-03-valantis-stex at review-bundle digest 11dd3b8f667da20aab1d343e804e7f53122ee64a5b0d086fc27a53445e05fe01 for admission. Reviewer: https://github.com/pranay5255.`

Until that exact approval is supplied, `review_status.yaml` remains `in_review`, the candidate is not copied into canonical EVMBench, no Harbor task is generated, and no agent/model smoke is run.
