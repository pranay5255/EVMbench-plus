# Missing-evidence report: Benqi Governance

Status: `blocked_missing_exact_snapshot`

Observed at: `2026-07-31T12:46:03Z`

The immutable source gates pass. The OCR JSONL is unchanged at SHA-256
`2de66fc23d5216db39fa0d492cebf886a57e9e2a7abd0ba81d87f2dd5b024522`;
all 29 records pass 19 global and 1,508 record checks. The 29-page PDF is
unchanged at SHA-256
`dd1ac726e8088bda57191043993fd9eba126f358d44156344d2ed3b56bc48128`.

The PDF annotations identify the intended repository and vulnerable commit:

- `https://github.com/aragon/benqi-governance`
- `ded42b671f112eef318482a8c9f10329d0aeef65`

That exact snapshot is unavailable. An isolated clone and authenticated
repository lookup return not found. Authenticated exact-commit, fix-commit,
repository/fork, public-code, and Aragon organization-inventory searches find
no matching snapshot. GitHub raw/codeload and a linked PR patch return `404`.
Software Heritage has no matching origin; Wayback availability has no relevant
capture; targeted local searches find no source tree; and none of 29 local Git
object databases contains the vulnerable commit.

A second, additive recovery pass is recorded in
`p3r1-external-index-recovery.json`. The ecosyste.ms commit lookup created an
unsynced placeholder row but recovered no commits; its issues index reports
`not_found`, while its packages and timeline indexes contain no usable record.
Sourcegraph returned no Solidity or exact-commit matches (with a documented
index-limit qualification). Exact npm, GitLab, Hugging Face, local Docker, and
the only separately indexed Benqi-governance gist author's public-repository
inventory also yielded no exact snapshot. None of these index checks replaces
the required Git object.

The final snapshot poll at `2026-07-31T13:15:01Z`, recorded in
`p3r2-final-snapshot-poll.json`, produced the same result: authenticated GitHub
repository and Git endpoints remain unavailable, exact repository/commit
searches remain complete with zero results, and the ecosyste.ms placeholder
remains unsynced with an empty commit listing.

An additional `gh api` CLI pass at `2026-07-31T13:35:16Z`, recorded in
`p3r3-gh-api-asset-and-code-recovery.json`, searched organization-wide release
assets, Actions artifacts, related audit repositories, repository metadata,
and three code-search query sets. Distinctive OCR/PDF snippets match the public
audit Markdown and its copies, while Solidity-filtered searches find no audited
contract source. Benqi-tagged Actions artifacts are expired frontend builds,
not the audited tree. GitHub Packages could not be ruled in or out because the
current token lacks `read:packages`; that scope limitation is treated as
ambiguous rather than negative evidence.

A Foundry pass at `2026-07-31T14:11:57Z`, recorded in
`p3r4-foundry-onchain-simulation.json`, used `cast` for historical storage,
log, ABI, and read-only call simulation on Avalanche C-Chain. The live proxy
was deployed after the audit, and the report's singular
`getGaugeByRewardController(address)` call is absent while a plural getter is
present. A simulated authorized `registerGauge` call succeeds on the later
runtime, but no transaction was broadcast and no source was recovered from
the runtime bytecode. This later, behaviorally different deployment is not
admissible evidence for the vulnerable Git snapshot.

The final authenticated `gh api` poll at `2026-07-31T14:15:58Z`, preserved in
`p3r5-final-authenticated-access-poll.json`, again returned `404` for the
repository and exact commit-object endpoints. Exact global commit search
returned zero complete results. No externally supplied access, official mirror,
or trusted bundle appeared, so the required detached checkout remains
unavailable.

GitHub's `404` does not distinguish an absent repository from one inaccessible
to the authenticated account. The evidence therefore supports
"unavailable to the current account and discovery sources," not "deleted."

P3 cannot prove the detached checkout, audited paths, submodules, framework,
or any finding against vulnerable code. Consequently:

- no candidate directory was created;
- no gold finding or OCR slice was materialized;
- no review-bundle manifest or approval digest exists;
- structural, semantic, build, and leakage checks were not run because their
  required candidate does not exist;
- no EVMBench admission, image, Harbor, verifier replay, agent/model run, or
  queue update occurred;
- the dirty canonical forestOfAudits checkout remained read-only.

## Required recovery

Provide one of:

1. repository access for the authenticated GitHub account, including any
   required Aragon organization SSO authorization;
2. an official public mirror containing the exact commit object;
3. a trusted Git bundle containing the exact commit and required submodules.

Do not substitute OCR, PDF snippets, report PoCs, fixed pull requests, a later
Aragon/BENQI tree, or deployed source without exact Git-object proof.
