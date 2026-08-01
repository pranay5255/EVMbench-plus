# Accountable source evidence and gate status

Status: `P1_repository_snapshot_blocked_P2_source_evidence_passed`

Review date: `2026-07-27`

This is a host-side missing-evidence and preflight record. It does not establish
gold findings or authorize candidate creation.

## Selected batch record

| Field | Value |
|---|---|
| Selection rank | `2` |
| PDF ID | `pdf_003641_b981ced0a4d4` |
| Category | `Lending/Credit` |
| Source filename | `2025-10-16-cyfrin-accountable-v2.0.pdf` |
| Source bucket | `other_audit_repo_pdfs` |
| Source page count | `37` |
| Indexed page count | `37` |
| Inventory vulnerability-page heuristic | `31` |
| Inventory unique-ID heuristic | `35` |
| PDF-confirmed report issue count | `33` |
| Intended mode | `detect` |

The inventory counts are discovery heuristics. The hash-verified PDF is
authoritative for report identity, scope, issue boundaries, and issue count.

## Immutable inputs

OCR JSONL:

`/home/experiments_base/OPD_base/outputs/evmbench_task_batch/extracted_pages/pdf_003641_b981ced0a4d4.jsonl`

Original PDF:

`/home/experiments_base/smart-contract-data/crawlers/output/repos/audit_repos/cyfrin-audit-reports/reports/2025-10-16-cyfrin-accountable-v2.0.pdf`

| Artifact | SHA-256 | Size/count result |
|---|---|---|
| OCR JSONL | `0c0ed8af4f1f0c90f62ea0b23e375c2aa2de2a7306941356a9dc0bf5ded28fcb` | 37 records |
| Source PDF | `5ff212c2abd0c2a690914ee7ae5e48fc18cfe8cb8662afde44788bf024034e90` | 37 physical pages |

All 37 populated `raw_record.source_abs_path` values resolve to the PDF path
above. The computed PDF hash equals every OCR row's
`source_pdf_sha256`.

## Gate 1: OCR JSONL

Result: `pass`

The read-only validator reported:

- schema `evmbench_task_creation.ocr_page.v1`;
- 37 parsed and valid records;
- one PDF ID;
- ordered, unique, exact page coverage `1..37`;
- 19 global checks with zero failures;
- 1,924 record checks with zero failures;
- exact top-level/raw-record duplicates;
- valid PDF and page-image SHA-256 fields;
- exact `text_length` values;
- SHA-256 before and after validation identical.

The persisted validator report uses project-neutral report schema
`ocr_to_evmbench_harbor.ocr_validation.v1`. Its validator unit tests pass.

## Gate 2: PDF verification and page map

Result: `pass`

`pdfinfo` reports an unencrypted, unrotated, 37-page PDF. Text extraction,
OCR-title extraction, link extraction, and visual inspection of the scope and
summary pages reconcile exported `page_number` values one-to-one with physical
pages.

| Exported/physical page(s) | Role |
|---|---|
| 1 | Report identity and version |
| 2–3 | Contents and finding index |
| 4–5 | Protocol, actors, components, and centralization context |
| 6 | Exact audited source-file scope and executive summary |
| 7–8 | Repository/commit summary, issue counts, and finding summary |
| 9–14 | Critical findings |
| 15–17 | High findings |
| 18–29 | Medium findings |
| 30–32 | Low findings |
| 33–36 | Informational findings |
| 37 | Gas optimization |

Pages 6–8 are scope/summary evidence. A summary title is not sufficient gold
evidence; each selected finding must use its full finding pages and vulnerable
code.

The completed P2 reports are:

```text
outputs/ocr-to-evmbench-harbor/_reports/2025-10-accountable/
  p2-ocr-validation.json
  p2-ocr-validation.txt
  p2-pdf-validation.json
  p2-pdf-ocr-review.md
  p2-ocr-corrections.json
```

They freeze all 33 finding page ranges. Five PDF-grounded transcription
corrections are recorded separately; the immutable JSONL was not edited.

## PDF-confirmed repository and snapshot claims

The report contains two related GitHub identities:

1. Scope/summary repository link:
   `https://github.com/Accountable-Protocol/credit-vaults-internal`
2. Vulnerable-code permalinks:
   `https://github.com/Accountable-Protocol/audit-2025-09-accountable`

Both point to vulnerable commit:

`fc43546fe67183235c0725f6214ee2b876b1aac6`

The fixed review commit is separate:

`1ae7e2fb74a3c0f543147e8793785b7f70d25070`

Do not use the fixed commit as `base_commit`, image `HEAD`, or part of the
detect task-group key.

## PDF-confirmed audited scope

The report lists these 20 production source files:

```text
src/access/AccessBase.sol
src/access/Authorizable.sol
src/access/Whitelistable.sol
src/constants/Errors.sol
src/factory/AsyncVaultFactory.sol
src/factory/FixedTermFactory.sol
src/factory/OpenTermFactory.sol
src/factory/RewardsFactory.sol
src/factory/StrategyFactoryBase.sol
src/modules/FeeManager.sol
src/modules/GlobalRegistry.sol
src/rewards/Rewards.sol
src/rewards/RewardsDistributorMerkle.sol
src/rewards/RewardsDistributorStrategy.sol
src/strategies/AccountableFixedTerm.sol
src/strategies/AccountableOpenTerm.sol
src/strategies/AccountableStrategy.sol
src/vault/AccountableAsyncRedeemVault.sol
src/vault/AccountableVault.sol
src/vault/queue/AccountableWithdrawalQueue.sol
```

This list must be checked against the vulnerable tree. It must not be widened
to all of `src/**` merely for convenience.

## GitHub API discovery

Read-only `gh api` checks on `2026-07-27` established:

- `repos/Accountable-Protocol/credit-vaults-internal` returns `404`;
- `repos/Accountable-Protocol/audit-2025-09-accountable` returns `404`;
- enumerating all currently visible `Accountable-Protocol` repositories yields
  only `safe-harbor` and `euler-price-oracle`, both unrelated;
- exact global commit search for
  `fc43546fe67183235c0725f6214ee2b876b1aac6` returns zero results;
- exact-name fork search for `audit-2025-09-accountable` returns zero results;
- GitHub raw and codeload URLs for the exact commit return `404`.

The configured GitHub CLI account `pranay5255` now authenticates
successfully. `gh api user` succeeds and the observed token scopes include
`repo` and `read:org`. Authenticated repository, commit, code, and fork
searches still return no result; both exact repository endpoints return `404`;
and the full repository inventory visible to the account contains no
Accountable or credit-vault match. The current account therefore lacks access
to the snapshot. A GitHub `404` does not distinguish deletion from an
unauthorized private repository.

The Cyfrin report itself remains retrievable through GitHub API at:

`Cyfrin/cyfrin-audit-reports/reports_md/2025-10-16-cyfrin-accountable-v2.0.md`

Its content object was observed as:

| Field | Value |
|---|---|
| Git blob SHA | `0b4de7681bd72a85e58beec71ac195b834591ca3` |
| Size | `92077` bytes |

That markdown corroborates report headings, descriptions, vulnerable-code
permalinks, and fix links. It is not a replacement for the missing repository
snapshot.

## Docker registry discovery

`docker.io/pranay5255/yudaii_evmbench` is an active public Docker Hub
repository. Its four current tags are the Valantis agent/verifier image and a
shared base image; none is Accountable-named or establishes the Accountable
Git commit. The exact registry response is summarized in:

`outputs/ocr-to-evmbench-harbor/_reports/2025-10-accountable/p1-docker-registry-discovery.json`

The registry is now the required destination for future Accountable images,
but it is not a source-snapshot substitute. No image was built or pushed.

## Gate 3 result

Result: `blocked`

The report provides one vulnerable commit and one explicit file scope, but the
repository component cannot yet be normalized or verified:

- the primary scope repository is unavailable;
- the audit mirror is unavailable;
- their shared commit object cannot be fetched;
- no local clone, Git bundle, or public fork containing that commit was found;
- no discovered local Git object database contains the commit, including
  packed or unreachable objects;
- code paths, submodules, build system, and vulnerable behavior therefore
  cannot be checked.

No valid task-group key has been resolved. The following is only an unresolved
claim and must not be treated as a task identity:

```text
UNRESOLVED_ACCOUNTABLE_REPOSITORY
  @ fc43546fe67183235c0725f6214ee2b876b1aac6
  | PDF-listed 20-file scope
  | detect
```

The formal P1 discovery record is:

```text
outputs/ocr-to-evmbench-harbor/_reports/2025-10-accountable/
  p1-snapshot-source.json
  p1-github-api-authenticated.txt
  p1-git-object-and-tree.json
  p1-submodules.json
  p1-scope-paths.json
  p1-adjacent-checkouts-read-only.txt
  p1-missing-evidence-report.md
```

## Hard stop

Because Gate 3 is blocked:

- do not create a candidate directory;
- do not write `H-*.md` or `gold_audit.md`;
- do not assign final finding IDs or awards;
- do not run the structural candidate validator;
- do not build or inspect an Accountable agent image;
- do not modify or admit into EVMBench;
- do not generate a Harbor task;
- do not run an agent/model.

Re-hash the OCR JSONL and PDF when work resumes and require the values above to
remain unchanged.
