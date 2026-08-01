# Phased task plan: Accountable EVMBench candidate and Harbor execution

Status: `P0_complete_P1_blocked_P2_complete`

Proposed candidate ID: `2025-10-accountable`

This plan is authorization-gated. Completing a phase does not authorize the
next phase, and no approval for another candidate applies here.

## Fixed inputs and compatibility pins

| Item | Required value |
|---|---|
| OCR JSONL SHA-256 | `0c0ed8af4f1f0c90f62ea0b23e375c2aa2de2a7306941356a9dc0bf5ded28fcb` |
| PDF SHA-256 | `5ff212c2abd0c2a690914ee7ae5e48fc18cfe8cb8662afde44788bf024034e90` |
| PDF/OCR pages | `37` / exact `1..37` |
| Vulnerable commit claim | `fc43546fe67183235c0725f6214ee2b876b1aac6` |
| Fixed commit, separate | `1ae7e2fb74a3c0f543147e8793785b7f70d25070` |
| Mode | `detect` |
| Compatible OPD_base revision | `38957485d5cd63dc5d664c3c2993f60b308f5776` |
| Compatible forestOfAudits revision | `1db91e36ec6f7c5975a8779b6ad930503c23e9d4` |
| Docker registry repository | `docker.io/pranay5255/yudaii_evmbench` |
| Candidate output root | `outputs/ocr-to-evmbench-harbor/` |
| Host-side report root | `outputs/ocr-to-evmbench-harbor/_reports/2025-10-accountable/` |

Use isolated clones at the pinned compatibility revisions. Inspect adjacent
checkouts before work and preserve every user-owned change. Never reset,
clean, stash, or overwrite them.

## Phase table

| Phase | Purpose | Current state | Approval boundary |
|---|---|---|---|
| P0 | Documentation and immutable-input preflight | Complete | Completed without candidate materialization |
| P1 | Recover and verify exact vulnerable Git snapshot | Blocked | Resume after repository access is granted or an exact snapshot is supplied |
| P2 | Revalidate OCR/PDF and freeze page map | Complete | Independent evidence gate passed; does not bypass P1 |
| P3 | Ground all findings and resolve one task key | Pending | Stop for disposition review if semantic ambiguity remains |
| P4 | Materialize host-side candidate | Pending | Requires P1–P3 pass and explicit authorization |
| P5 | Structural, semantic, image, and leakage validation | Pending | Produces human review bundle only |
| C1 | Digest-bound human candidate review | Pending | Mandatory hard stop |
| P6 | Bind approval and revalidate | Pending | Requires exact candidate/digest approval plus reviewer identity |
| P7 | Isolated EVMBench admission and registry check | Pending | No canonical mutation unless separately requested |
| P8 | Build and inspect immutable images | Pending | Must pass offline and leakage gates |
| P9 | Generate exactly one Harbor task | Pending | Empty isolated destination only |
| P10 | Harbor load and contract verification | Pending | Requires pinned Harbor version/schema |
| P11 | Explicit agent/model smoke | Pending | Requires explicit smoke pair |
| P12 | Final integrity and provenance closeout | Pending | Completion only after all artifacts pass |

## P0: Documentation and input preflight

Completed:

- read the full OCR-to-EVMBench/Harbor operational contract;
- verified the selected rank-2 batch record;
- validated all 37 OCR rows and exact input immutability;
- hash-verified the 37-page source PDF;
- reconciled scope, summary, and finding headings;
- extracted full vulnerable and fixed commit links from the PDF;
- used GitHub API for repository, commit, fork, and canonical report checks;
- accounted for all 33 findings in a preliminary worksheet;
- created this PRD and phase plan.

Exit state:

`repository_snapshot_blocked`

No candidate, image, EVMBench admission, Harbor task, or smoke artifact exists.

## P1: Recover exact vulnerable repository snapshot

Required input:

- authenticated access to the original repository; or
- an official public mirror containing the exact commit object; or
- a trusted Git bundle containing the exact commit and required submodules.

Procedure:

1. Create a fresh isolated review directory under `/tmp`.
2. Record supplied artifact path/URL, size, and SHA-256 before use.
3. Verify repository origin claims without rewriting them.
4. Run `git cat-file -e
   fc43546fe67183235c0725f6214ee2b876b1aac6^{commit}`.
5. Check out that commit detached and require exact `HEAD`.
6. Record commit, parent(s), root tree, and repository status.
7. Initialize recursive submodules at pinned revisions.
8. Verify every PDF-listed source path exists.
9. Determine whether `credit-vaults-internal` and
   `audit-2025-09-accountable` are the same Git history/tree.
10. Select one canonical repository identity only from verified evidence.

Reject:

- source reconstructed from the PDF or OCR;
- current deployed/verified source without exact commit proof;
- a fixed or later snapshot;
- an archive missing provenance sufficient to bind it to the commit;
- a dirty or branch-substituted checkout;
- missing required submodules or scope files.

Required reports:

```text
p1-snapshot-source.json
p1-git-object-and-tree.json
p1-submodules.json
p1-scope-paths.json
p1-adjacent-checkouts-read-only.txt
```

Additional authenticated discovery evidence is retained in
`p1-github-api-authenticated.txt`.

Current result:

`blocked_missing_exact_snapshot`

All required P1 report paths exist, but the commit/tree/submodule/scope
evidence fields remain fail-closed. Authenticated GitHub API checks using a
valid `repo`-scope token, plus archive, dataset, container, and local searches,
did not recover the exact object. Neither repository is accessible to the
configured account, and its full visible repository inventory contains no
matching snapshot. A direct `git cat-file` sweep of every local object database
also found no packed or unreachable copy of the vulnerable commit.

Exit criterion: one exact clean vulnerable checkout and one canonical
repository URL.

## P2: Revalidate source evidence and freeze page roles

1. Recompute OCR and PDF hashes.
2. Re-run all OCR invariants from a clean compatible OPD_base checkout.
3. Reconfirm PDF physical page count.
4. Compare scope and every retained finding page against the PDF.
5. Record OCR transcription corrections without editing JSONL.
6. Freeze exact scope-page and finding-page boundaries.
7. Recompute both source hashes after review.

Required reports:

```text
p2-ocr-validation.json
p2-ocr-validation.txt
p2-pdf-validation.json
p2-pdf-ocr-review.md
p2-ocr-corrections.json
```

Current result:

`complete`

All five required P2 reports exist. OCR validation passed 37/37 records with
zero failures; the PDF remained hash-identical at 37 pages; all 33 finding
ranges were reconciled; and five PDF-grounded OCR corrections were recorded
without modifying the preserved JSONL.

Exit criterion: exact-checksum evidence remains unchanged and every relevant
page boundary is reviewer-readable.

## P3: Code-ground dispositions and task-group resolution

1. Verify each of the 33 findings in the vulnerable tree.
2. For `candidate`/`hold` rows, prove reachability and asset-loss sequence.
3. For preliminary exclusions, confirm the code does not establish a stronger
   loss path.
4. Inspect report-linked fix commits only as separate corroboration.
5. Resolve the four mandatory merge/split clusters.
6. Assign deterministic `H-01...H-N` only after distinctness is final.
7. Require all included findings to be inside the exact audited scope.
8. Produce a disposition for every report item.
9. Resolve exactly one task-group key.

Required reports:

```text
p3-repository-snapshot.json
p3-finding-grounding.md
p3-report-dispositions.json
p3-task-group.json
p3-fix-corroboration.json
```

Exit criterion:

- 33/33 findings dispositioned;
- zero unresolved included findings;
- all included roots distinct and asset-loss relevant;
- exactly one repository/commit/scope/detect key.

If any semantic or repository ambiguity remains, stop without P4.

## P4: Materialize the in-review candidate

Authorization required before this phase.

1. Create only
   `outputs/ocr-to-evmbench-harbor/2025-10-accountable/`.
2. Write `config.yaml`, `.dockerignore`, `Dockerfile`,
   `provenance.json`, and `review_status.yaml`.
3. Write one `findings/H-*.md` per selected distinct root.
4. Build `findings/gold_audit.md` deterministically.
5. Copy exact ordered OCR rows into scope/finding slices.
6. Set `state: in_review`, `human_approved: false`, and no approver.
7. Generate a file manifest containing path, size, and SHA-256.

Exit criterion: one internally consistent host-side candidate; no approval,
admission, or Harbor state.

## P5: Validate candidate, repository, and visibility boundary

1. Run the compatible structural validator without
   `--require-approved`.
2. Verify selected count equals config, gold files, provenance, and intended
   grader `max_score`.
3. Verify every evidence reference resolves and every slice is byte-exact.
4. Build the agent image from a minimal candidate-specific context.
5. Verify repository `HEAD`, scope, submodules, and offline build/tests.
6. Inspect Dockerfile, context, image history, every layer, filesystem, Git
   refs, and reachable commits.
7. Reject PDF/OCR/gold/provenance/review/fix/credential leakage.
8. Create a deterministic review manifest and digest.

Required reports include:

```text
p5-structural-validator.json
p5-semantic-validation.json
p5-repository-validation.json
p5-offline-build.log
p5-offline-test.log
p5-image.json
p5-leakage-scan.json
c1-review-manifest.json
c1-review-bundle-digest.txt
c1-review-report.md
```

Exit criterion: review-ready only. Stop at C1.

## C1: Human candidate review

Reviewer must compare:

- source hashes and exact PDF pages;
- vulnerable checkout identity and code;
- all 33 dispositions;
- every selected gold finding;
- merge/split decisions and award count;
- agent-image contents and leakage report;
- deterministic review-manifest digest.

Approval must bind the candidate and exact digest, for example:

```text
I approve candidate 2025-10-accountable at review-bundle digest
<sha256> for admission. Reviewer: <verifiable reviewer identity>.
```

Any revision invalidates the prior digest and requires a new review bundle.

## P6: Bind approval and revalidate

Only after exact C1 approval:

1. Set `approved_for_admission`, `human_approved: true`, and `approved_by`.
2. Mirror state in provenance.
3. Run structural validation with `--require-approved`.
4. Re-run source, repository, count, manifest, and leakage integrity.
5. Record approval binding and approved-file manifest.

Stop on any byte drift or identity mismatch.

## P7: Isolated EVMBench admission

1. Clone forestOfAudits at
   `1db91e36ec6f7c5975a8779b6ad930503c23e9d4` into `/tmp`.
2. Admit only the approved candidate into the explicit isolated EVMBench
   target.
3. Inspect the exact diff.
4. Load through the canonical audit registry.
5. Confirm IDs, titles, awards, gold files, base commit, and split membership.
6. Record the isolated EVMBench commit/state.

Do not modify the canonical sibling checkout merely because isolated admission
passes.

## P8: Build and inspect immutable images

1. Build the exact approved agent image.
2. Build a separate verifier image when required.
3. Tag them only under `pranay5255/yudaii_evmbench` using
   `2025-10-accountable-agent-<content-id>-amd64` and
   `2025-10-accountable-verifier-<content-id>-amd64`.
4. Verify vulnerable `HEAD` and no post-audit reachable history.
5. Run repository build/tests offline.
6. Scan context, layers, images, and runtime filesystem for leakage.
7. Push only after the preceding checks pass; never use or overwrite `latest`.
8. Resolve the remote manifests and require local/remote digest agreement.
9. Pin Harbor references by immutable digest.
10. Record tags, digests, base image identities, push results, and test
    results.

The user-selected registry does not waive P1–P7 or constitute C1 approval.

## P9: Generate exactly one Harbor task

1. Choose an empty isolated output directory.
2. Run the canonical adapter for only `2025-10-accountable`.
3. Require exactly one directory:
   `evmbench__detect-2025-10-accountable`.
4. Reject any second or unexpected output.
5. Inspect the generated tree and complete visibility boundary.
6. Record any adapter compatibility patch in an isolated checkout diff.

Do not use `--overwrite` against a broad, unresolved, or user-owned
destination.

## P10: Harbor load and contract checks

1. Pin the exact Harbor distribution and wheel/package hash.
2. Resolve the schema-version compatibility gate.
3. Load the task through Harbor's task model.
4. Confirm audit ID, detect mode, image digests, no-network agent policy,
   resources, timeouts, submission path, and separate verifier policy.
5. Verify `tests/test.sh` emits numeric reward on success and expected failure.
6. Verify detailed grade artifact retention.
7. Re-run generated-tree leakage scans.

Exit criterion: exactly one loadable task with a complete verifier contract.

## P11: Explicit agent/model smoke

Requires a user-supplied agent and model for this candidate.

1. Run one task with concurrency one.
2. Require no runtime network for the agent.
3. Confirm repository inspection and writable submission path.
4. Require `audit.md`, numeric reward, and full grade JSON.
5. Confirm `max_score` equals the approved selected count.
6. Record false positives/negatives for human review.
7. Record job ID, agent/model, task path, tool version, image digests, and
   artifacts.

A structurally successful run with missing grade artifacts is a failure.

## P12: Final integrity closeout

1. Recompute immutable input hashes.
2. Recompute approved candidate and generated-task manifests.
3. Verify image digests and EVMBench state.
4. Re-run visibility scans.
5. Confirm no canonical/user-owned checkout was unintentionally changed.
6. Write final machine-readable and reviewer-readable summaries.

Completion requires every PRD acceptance criterion. If canonical publication
or mutation is desired after isolated success, request it separately with an
explicit target.

## Global stop conditions

Stop immediately on:

- OCR/PDF checksum drift;
- missing or ambiguous repository identity;
- vulnerable commit mismatch;
- missing audited path or submodule;
- finding without reachable code or concrete asset-loss path;
- unresolved merge/split affecting score count;
- dirty admission target;
- candidate/review digest drift;
- any evidence or answer leakage;
- unsupported Harbor schema/version;
- more than one generated task;
- missing submission, reward, or full grade artifact.
