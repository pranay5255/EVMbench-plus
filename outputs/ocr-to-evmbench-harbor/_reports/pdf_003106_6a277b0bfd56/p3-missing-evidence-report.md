# Agora StableSwap pre-candidate Gate 3 failure

Result: **fail closed before candidate creation**.

The immutable OCR and PDF gates pass, and the PDF gives an unambiguous intended
repository, commit, Solidity scope, and `loss_of_assets` task identity. The
exact vulnerable Git object is unavailable after bounded recovery, so the
workflow cannot independently verify the code, build, scope, or findings.

## Passed evidence gates

- The OCR JSONL has 29 ordered records covering exactly pages 1–29. All 19
  global checks and all 1,508 record checks passed. Its before/after SHA-256 is
  `8c84ce19523648894955bc608f0721afd77d257ac5b0a6c121ccbb474658fda1`.
- The original PDF is present, readable, unencrypted, and has 29 physical
  pages. Its SHA-256 exactly matches the inventory:
  `a985d452fac4a3490c7186390a475da0cdf7fc9258c177310505a46909f5ba41`.
- Every PDF page and OCR row was compared by exported page number. Rendered PDF
  pages were used to confirm the report identity, repository, exact commits,
  scope, finding inventory, and representative finding text.
- The PDF names repository
  `https://github.com/amphora-atlas/stable-swap-dev`, vulnerable commit
  `1dedf62430e2fcf164a807f95c80c12615bad135`, and separate fixes-review commit
  `0b424f359bc22a80f681a92440cf5746e5b7dcf8`.
- The PDF limits scope to five Agora StableSwap contracts and reports one
  Medium plus fifteen Low findings.

## Failed invariant: exact audited snapshot unavailable

The report-linked repository returns GitHub `404`, its forks endpoint is
unavailable, and Git cannot fetch the exact SHA. GitHub's commit index has no
match. A noninteractive SSH probe also fails with `Permission denied
(publickey)`, so no separate authorized key on this host exposes the canonical
repository. The same exact-object check fails in every discovered code-bearing
candidate:

- `DrakeEvans/stable-swap-dev` and its sole fork
  `0xMacro/agora-stable-swap-dev`;
- the public related repository `agora-finance/stable-swap`.

All branches, tags, pull refs, releases, and workflow artifacts exposed by
those repositories were checked. Direct Git smart-protocol fetches of the
audited SHA from all three return `upload-pack: not our ref`. Neither the
vulnerable SHA nor the separate fixed SHA exists in them. Similar current
source cannot replace the audited tree.

Software Heritage has neither the canonical origin nor either revision. Exact
web search returned no SHA match. A historical public-GitHub-event query
returned no records for the canonical repository, and GitHub code search for
the exact SHA or report proof-of-concept finds only Pashov's report Markdown,
not a source repository. Ten caller-local Git roots contain no such commit, no
matching local bundle/archive exists, and the local Docker inventory contains
no Agora image. Four dangling images were identified by build-layer history as
Recall Labs or Gitcoin/Loop images, not Agora.

Without a detached checkout whose `HEAD` is exactly the audited commit, the
workflow cannot establish root tree, parents, submodules, clean build, audited
paths, or whether any report claim is present and exploitable in the required
snapshot. PDF snippets, OCR, current successor source, and the separate fixed
SHA are not admissible substitutes.

## Prohibited downstream state

- Candidate ID: none.
- Review-bundle approval digest: none. Any digest for this directory is
  pre-candidate gate evidence and is not approvable for admission.
- Selected/code-grounded findings and gold audit: none.
- Candidate validator, source build, Docker build, image leakage checks,
  registry publication, EVMBench admission, Harbor generation/loader/replay,
  and model smoke: not run because no vulnerable checkout or candidate exists.
- Dirty canonical `forestOfAudits`/EVMBench checkout: inspected read-only and
  untouched.
- No costly agent or model run was launched.

To resume, provide a trusted public origin or content-addressed Git bundle that
contains the complete object
`1dedf62430e2fcf164a807f95c80c12615bad135`. Recovery must still be followed
by detached-HEAD, tree/parent, submodule, build, scope, and finding review. The
canonical queue ordering remains Benqi Governance next; Agora is an out-of-order
blocked review, not evidence that Benqi or Burve changed state.
