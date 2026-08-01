# EVMbench++ Task Workspace

This directory is an independent private Git repository nested inside the
`OPD_base` workspace. The parent repository ignores `/task_dir/`; task
artifacts are versioned and published only from this repository, while parent
pipeline documentation and the selected-task queue remain in `OPD_base`.

## Artifact layout

- `scripts/` and `tests/` contain local evidence validators and their tests.
- `outputs/ocr-to-evmbench-harbor/<candidate-id>/` contains reviewed EVMBench
  candidate packages.
- `outputs/ocr-to-evmbench-harbor/_reports/` contains validation, approval,
  admission, image, leakage, and execution evidence, including fail-closed
  reports for blocked tasks.
- `outputs/ocr-to-evmbench-harbor/_harbor/` contains generated Harbor exports
  and explicitly retained superseded exports.
- `temp_docs/` contains task-scoped precursor and review documents that remain
  relevant to the corresponding task history.

Source PDFs, OCR records, gold findings, provenance, review decisions, and
other authoring evidence are private host-side material. Their presence in
this repository does not make them agent-visible: candidate Docker contexts,
runtime images, and Harbor exports must continue to enforce the documented
evidence-leakage boundary.

## Publishing contract

Create and review tasks directly under this directory. After a task reaches an
evidence-backed created or blocked milestone:

1. confirm the repository root with `git rev-parse --show-toplevel`;
2. run the relevant validators, secret scan, and large-file scan;
3. stage only that task's explicit candidate, Harbor, report, precursor, and
   superseded paths;
4. inspect `git diff --cached --name-status` and commit one task identity or
   later milestone at a time; and
5. push from this nested repository only.

Never use `git add .` or `git add -A`, never mix task identities in one commit,
and never stage this directory from the parent `OPD_base` repository. Evidence
`.log` files and intentional task outputs are trackable; only local caches,
environments, secrets, coverage output, and editor metadata are ignored.
