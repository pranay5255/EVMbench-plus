# C1 human review: `2025-07-securitize-onofframp`

The pre-approval workflow is complete and stopped at the mandatory human gate.
No EVMBench admission, Harbor generation, registry publication, or agent/model
run has occurred.

## Approval-bound identity

- Candidate: `2025-07-securitize-onofframp`
- Review-manifest SHA-256 (review-bundle digest):
  `1e7a1c634591a268032ec3970839514f558df2635c3ebe985754f7c4ed20b404`
- Repository: `https://github.com/securitize-io/bc-on-off-ramp-sc.git`
- Vulnerable commit: `a944bb11b106c13a5e43f8de01c9c01eeb5bb472`
- Task-key SHA-256:
  `dec131fd32621786fc81c70656791670b78b7b5cd706befe0d6749bb5dd329ab`
- Mode/framework/policy: `detect` / Hardhat / `loss_of_assets`

Approval is valid only if it names the candidate, exact manifest digest, and
reviewer identity.

Suggested approval phrase:

```text
I approve candidate 2025-07-securitize-onofframp at review-bundle digest
1e7a1c634591a268032ec3970839514f558df2635c3ebe985754f7c4ed20b404 for admission.
Reviewer: <identity>.
```

## Source evidence

| Item | Value |
|---|---|
| Rank | 18 (canonical next) |
| PDF SHA-256 | `3eae87e40dbad4acefcdf4175e3a943bffebd23272755b41fa881fbe817f27c6` |
| OCR SHA-256 | `10378faf737b4757af74693161c77d8c66c76c98aa9309eb31cd80813b07433c` |
| Pages | 27 / 27 |
| Report | Cyfrin Securitize On-Off Ramp and Bridge v2.1 — 23 Jul 2025 |

OCR is host-side discovery evidence. JSONL was not rewritten. PDF link
annotations supply fix-commit URLs that identify
`securitize-io/bc-on-off-ramp-sc`; the summary-table commit prefix
`a944bb11b106` uniquely resolves to the full vulnerable SHA above.

## Selected findings

| ID | Report | Pages | Title |
|---|---|---:|---|
| H-01 | C-1 / 7.1.1 | 10–11 | Missing nonce validation allows EIP-712 subscription replay and double asset transfers |

## Exclusions (summary)

- M-1, M-4, and all Low/Informational on-off-ramp items: no verified
  `loss_of_assets` path (availability, config hygiene, docs, style).
- M-2, M-3 and other bridge items: separate Bitbucket repository
  `bc-securitize-bridge-sc` with no public exact snapshot; held as a
  different task-group identity, not merged into this candidate.

## Validator results

- OCR validator: PASS (27/27 records; immutable hash match)
- PDF hash + page count: PASS
- Structural `validate_evmbench_candidate.py`: PASS (`in_review`)
- Leakage (Dockerfile / dockerignore): PASS (no COPY/ADD of gold; deny-all context)
- Semantic code grounding for H-01: PASS at detached HEAD
- Hardhat compile: **FAIL** — `@securitize/digital_securities@3.1.4` returns HTTP 404
  on registry.npmjs.org (with the repository's checked-in `.npmrc` token as well).
  Dockerfile therefore pins source only and does not run `npm ci` at image build.

## Unresolved risks

1. **Bridge task group unresolved.** Exact public Git object for
   `60b6ef00e8a8…` on `bc-securitize-bridge-sc` was not recovered. Do not
   treat M-2/M-3 as admitted here.
2. **Private npm dependency unavailable.** Full compile/tests cannot be proven
   without `@securitize/digital_securities@3.1.4`. Agent image is source-pinned
   for offline inspection; post-approval may need a recovered package tarball
   or interface stubs if compile is required.
3. **Upstream `.npmrc` token.** The public audited tree contains an npm auth
   token. Image build clones from GitHub rather than copying host worktrees.
4. **Path prefix mapping.** Report lists `bc-on-off-contracts\…`; repository
   uses `contracts/…`. Verified by tree presence, not by identical strings.

## Confirmation

- Canonical `forestOfAudits` checkout was not modified for admission.
- No Harbor artifacts were generated.
- No agent/model smoke was launched.
- Candidate remains `state: in_review` / `human_approved: false`.
