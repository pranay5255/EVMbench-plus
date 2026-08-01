# PRD: Accountable detect task for EVMBench and Harbor

Status: `draft_P2_complete_blocked_on_exact_repository_snapshot`

Proposed candidate ID: `2025-10-accountable`

Mode: `detect`

Primary evidence: one hash-verified PDF and its preserved 37-page OCR JSONL.

## Objective

Create one reproducible EVMBench detect task in which an auditing agent
inspects the exact vulnerable Accountable repository snapshot and reports
distinct, code-grounded vulnerabilities with direct or indirect
loss-of-assets impact. After digest-bound human approval, admit that one
candidate into an isolated compatible EVMBench checkout, generate exactly one
Harbor task, and complete a no-network smoke run with an explicitly selected
agent and model.

## Current blocker

The vulnerable commit and audited file list are PDF-confirmed, but neither
report-linked GitHub repository is currently accessible and no exact snapshot
has been recovered. Candidate materialization is forbidden until the
repository gate in
[01_SOURCE_EVIDENCE_AND_GATE_STATUS.md](01_SOURCE_EVIDENCE_AND_GATE_STATUS.md)
passes.

P2 source verification is complete: the OCR/PDF hashes remain unchanged, all
37 OCR records pass validation, and all 33 finding page ranges are frozen.
This evidence pass does not relax the repository gate.

## Non-goals

- Patch or exploit mode.
- Combining a second PDF under the version-1 provenance contract.
- Reconstructing the repository from report snippets, OCR, verified deployed
  bytecode/source, or a later fixed release.
- Treating report severity as automatic EVMBench inclusion.
- Scoring availability, compliance, style, gas, or centralization findings
  without a concrete asset-loss path.
- Modifying dirty or canonical user-owned checkouts during review.
- Inferring approval from these documents, a validator pass, or prior work on
  another candidate.

## Task identity requirements

The final task-group key must contain exactly:

```text
normalized canonical repository URL
+ fc43546fe67183235c0725f6214ee2b876b1aac6
+ exact PDF-listed 20-file audited scope
+ detect
```

The fixed commit
`1ae7e2fb74a3c0f543147e8793785b7f70d25070` is host-side corroboration only.

If the original source repo and audit mirror are both recovered, compare their
commit objects and trees before choosing one normalized repository identity.
Do not select a convenient mirror without proof that it contains the audited
snapshot.

## Users and review roles

- Author: prepares host-side evidence, candidate files, and validation
  reports.
- Human reviewer: compares PDF, OCR boundaries, and exact vulnerable code;
  decides finding inclusion, merge/split, and approval.
- Auditing agent: sees only generic instructions and the pinned vulnerable
  repository.
- Verifier: sees the approved gold findings and agent submission, and emits
  numeric Harbor reward plus full grade details.

The approver identity must be explicit and must not be filled automatically.

## Functional requirements

### FR-1: Immutable evidence

- Hash OCR and PDF before and after authoring.
- Preserve the original JSONL byte-for-byte.
- Copy selected JSONL rows byte-for-byte and in page order.
- Keep all PDF/OCR material host-side.
- Record every PDF/OCR correction separately; never normalize the source.

### FR-2: Exact vulnerable repository

- Use an isolated clone or Git bundle worktree.
- Check out the vulnerable commit detached.
- Verify commit and root-tree IDs.
- Initialize and verify every pinned submodule.
- Verify all 20 audited source files.
- Record included/excluded paths and build dependencies.
- Prove the final agent image repository `HEAD` equals the vulnerable commit.

### FR-3: Finding selection

- Account for all 33 report findings.
- Include only reachable, distinct root causes with concrete asset-loss paths.
- Give every exclusion and merge/split a code-grounded reason.
- Treat fix commits as corroboration, not vulnerable task inputs.
- Freeze the selected count only after the merge/split clusters in the
  worksheet are resolved.
- Set EVMBench `max_score` to the final distinct selected count.

### FR-4: Host-side candidate

Only after Gates 1–3 pass, create:

```text
outputs/ocr-to-evmbench-harbor/2025-10-accountable/
  .dockerignore
  config.yaml
  Dockerfile
  provenance.json
  review_status.yaml
  findings/
    H-01.md
    ...
    gold_audit.md
  ocr_evidence/
    pdf_003641_b981ced0a4d4/
      scope.pages.jsonl
      H-01.pages.jsonl
      ...
```

Initial review state:

```yaml
state: in_review
human_approved: false
approved_by: null
```

Candidate `config.yaml` must use `mode: detect`, the vulnerable base commit,
non-empty vulnerability titles, and one documented equal-weight award policy
unless the reviewer approves another policy.

### FR-5: Gold finding quality

Each `H-*.md` must identify:

- affected audited files, contracts, and functions;
- concise root cause;
- attacker or failure prerequisites;
- exploit/failure sequence;
- direct or indirect asset-loss impact;
- exact vulnerable-code evidence;
- remediation only when it helps distinguish the root cause.

`gold_audit.md` must be the ordered combination of the individual approved
findings. Config count, files, provenance, and grader count must agree.

### FR-6: Agent-visible environment

The final image may contain:

- the exact vulnerable repository;
- pinned submodules and required offline build dependencies;
- tools promised by the generic instruction.

It must not contain, in any layer or renamed form:

- PDF files, text, page images, paths, hashes, or ranges;
- OCR JSONL, OCR text, `<PAGE>`, or `<|det|>` data;
- this `temp_docs` tree;
- provenance, review status, or reviewer notes;
- `findings/`, finding IDs/titles, `gold_audit.md`, or grader gold;
- post-audit fixes or a reachable fixed branch;
- credentials or host provenance.

Use a candidate-specific minimal Docker context. A broad task-directory context
is prohibited.

#### Image registry and publication

Use this Docker Hub repository for Accountable agent and verifier images:

`docker.io/pranay5255/yudaii_evmbench`

Use content-specific tags:

```text
pranay5255/yudaii_evmbench:2025-10-accountable-agent-<content-id>-amd64
pranay5255/yudaii_evmbench:2025-10-accountable-verifier-<content-id>-amd64
```

Never publish `latest` or overwrite an existing content tag. Harbor must
ultimately reference the pushed manifest digest, not a mutable tag. Before
`docker push`, verify the exact vulnerable `HEAD`, offline build/tests, complete
context and layer leakage scans, and local/remote digest agreement.

The registry selection is not human candidate approval. No Accountable image
may be built or pushed while the exact repository snapshot gate is blocked.

### FR-7: Agent instruction and submission

`instruction.md` must say only that the task is detect-only, identify the
repository path and exact in-scope files, and require findings to contain root
cause, affected code, exploit/failure sequence, and asset-loss impact.

Required canonical submission:

`/home/agent/submission/audit.md`

A structured `/home/agent/submission/audit.json` using an explicitly versioned
schema may be retained as a non-reward-gating companion if the reviewer
approves it. Markdown remains the grader input unless the EVMBench contract is
deliberately changed and revalidated.

The instruction must not reveal report IDs, titles, severities, issue count,
page evidence, gold phrases, or fix commits.

### FR-8: Harbor task

Generate exactly:

```text
evmbench__detect-2025-10-accountable/
  instruction.md
  task.toml
  environment/
    README.md
  tests/
    test.sh
    evmbench_harbor_verifier.py
    ...
```

Requirements:

- pin an immutable agent-image digest;
- use `network_mode = "no-network"` for the agent environment;
- use a separate verifier environment when gold/grader material is required;
- declare CPU, memory, storage, and timeouts;
- write numeric `/logs/verifier/reward.json` or `reward.txt`;
- retain a full EVMBench grade artifact;
- fail safely for missing or malformed submissions;
- expose only declared submission/artifact paths to the verifier.

The target Harbor version and supported task schema must be pinned and loaded
before smoke execution. Local evidence shows Harbor `0.20.0` successfully
loaded a schema `1.3` EVMBench task, while the authoring guideline cites schema
`1.4`. Treat this as a compatibility gate, not permission to claim parity.
Generate for and validate against one explicit chosen version.

Provisional resource starting point, subject to measurement:

| Resource | Starting value |
|---|---:|
| Agent timeout | 3600 seconds |
| Verifier timeout | 900 seconds |
| CPU | 4 |
| Memory | 16384 MB |
| Storage | 20480 MB |
| GPU | 0 |

### FR-9: Human approval and admission

Before approval:

- run the compatible structural validator without `--require-approved`;
- validate repository HEAD, scope, finding count, semantics, and byte-exact
  evidence slices;
- inspect Docker context and image layers;
- create a deterministic review manifest and SHA-256;
- stop for exact candidate-and-digest-bound approval.

After explicit approval and reviewer identity:

- update review state and mirrored provenance;
- run the validator with `--require-approved`;
- re-run integrity and leakage checks;
- admit only into an explicit isolated compatible EVMBench checkout;
- inspect the admission diff;
- load through the canonical registry;
- build and inspect the exact agent/verifier images;
- generate into an empty isolated Harbor output directory.

### FR-10: Smoke execution

An agent and model must be explicitly supplied for this candidate. Do not reuse
another candidate's smoke pair by implication.

The smoke is successful only when:

- exactly one task loads;
- the agent inspects the vulnerable repository offline;
- `audit.md` is created at the required path;
- numeric reward and full grade JSON are produced;
- `max_score` equals the approved distinct finding count;
- image digests, EVMBench commit, Harbor version/schema, task path, and job
  result are recorded;
- OCR/PDF/gold leakage remains zero.

## Non-functional requirements

- Reproducibility: exact hashes, commits, tree IDs, image digests, tool
  versions, and manifests.
- Isolation: no mutation of dirty adjacent or canonical checkouts.
- Fail-closed behavior: missing evidence, ambiguity, dirty targets, count
  mismatch, unexpected second task, or leakage is a hard stop.
- Auditability: machine-readable reports plus concise reviewer-readable
  summaries.
- Offline runtime: agent repository inspection and promised checks work without
  network access.

## Acceptance criteria

The task is complete only when all are true:

- one exact repository/commit/scope/mode key is proven;
- all 33 report findings have final code-grounded dispositions;
- every selected finding is reachable, distinct, and asset-loss relevant;
- source evidence is unchanged;
- candidate structural, semantic, repository, and leakage gates pass;
- digest-bound human approval is recorded;
- isolated EVMBench registry/build checks pass;
- exactly one Harbor task loads with the pinned version/schema;
- one explicit agent/model smoke produces submission, reward, and full grade;
- final provenance records all immutable identities.

## Open decisions

These are deliberately unresolved:

- canonical repository URL after snapshot recovery;
- final selected finding count and `H-*` mapping;
- merge/split decisions for the four worksheet clusters;
- optional JSON submission schema;
- exact image base and offline dependency strategy;
- exact Harbor version/schema pair;
- smoke agent and model;
- reviewer identity.
