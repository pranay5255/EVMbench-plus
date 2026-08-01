# P3 repository grounding: Benqi Governance

Status: `blocked_missing_exact_snapshot`

The checksum-verified PDF identifies repository
`https://github.com/aragon/benqi-governance` and vulnerable commit
`ded42b671f112eef318482a8c9f10329d0aeef65`. The ten audited paths are exact
at the report layer, but no detached checkout can be produced.

An isolated clone returned `Repository not found`. The active authenticated
GitHub account can query the API and has `repo` and `read:org` scopes, yet the
repository endpoint returns `404`; exact vulnerable/fix commit searches,
repository/fork searches, public code searches, and the visible Aragon
organization inventory return no match. Raw, codeload, and a report-linked PR
patch also return `404`.

Software Heritage has no matching origin. Wayback availability checks have no
repository, commit, tree, or linked-PR capture around the audit. Targeted local
filesystem searches found no source tree, and none of 29 local Git object
databases contains the vulnerable commit.

The additive recovery record `p3r1-external-index-recovery.json` closes further
public-index routes. ecosyste.ms has no synced commit, issue, package, or
timeline material for this repository; Sourcegraph returned no Solidity or
exact-commit match, subject to its reported index-limit warning; and exact npm,
GitLab, Hugging Face, local Docker, and related-account inventory checks found
no source snapshot. A denied anonymous GHCR manifest lookup is explicitly
treated as ambiguous and supplies no admissible evidence.

The `gh api` asset and code-search pass is recorded in
`p3r3-gh-api-asset-and-code-recovery.json`. It enumerated 210 visible Aragon
repositories, 1,014 releases, 232 release assets, and 5,389 Actions artifacts.
No asset matched the audited commit or contract tree. All 37 Benqi-tagged
artifacts were expired `aragon/app` frontend builds. High-entropy OCR/PDF code
searches matched the official audit Markdown and copies of it, plus frontend
ABI/hooks; Solidity-filtered searches found no audited source. These are useful
snippet-to-report matches but not Git-object evidence.

The additive Foundry pass is recorded in
`p3r4-foundry-onchain-simulation.json`. `cast` identified a live Avalanche
proxy and simulated an authorized `registerGauge` call without broadcasting.
That proxy was deployed after the audit, and its plural
`getGaugesByRewardController(address)` selector differs from the singular
`getGaugeByRewardController(address)` named in the OCR/PDF. The singular call
reverts on the live runtime. Blockscout's deployed-bytecode source search also
returned no implementation source. The simulation is useful behavioral
corroboration for a later deployment, but the date and ABI mismatch prevent it
from substituting for the exact audited tree.

The final authenticated access poll at `2026-07-31T14:15:58Z` is recorded in
`p3r5-final-authenticated-access-poll.json`. The current `gh api` account is
still `pranay5255` with `repo` and `read:org` scopes. Both the repository and
exact Git-commit-object endpoints return `404`, while an exact global commit
search is complete with zero results. This reaffirms unavailability to the
current account; it does not distinguish deletion from private or SSO-gated
access.

This evidence means only that the snapshot is unavailable to the current
authenticated account and discovery sources. It does not prove that the
repository was deleted rather than made private or otherwise access-restricted.

P3 therefore cannot verify:

- the commit object, parents, and root tree;
- detached checkout `HEAD`;
- the ten in-scope paths in that tree;
- submodules and dependency pins;
- the repository's actual build/test framework;
- any report finding against vulnerable code.

No replacement repository, fixed commit, report snippet, or reconstructed tree
is admissible under the exact-snapshot gate.
