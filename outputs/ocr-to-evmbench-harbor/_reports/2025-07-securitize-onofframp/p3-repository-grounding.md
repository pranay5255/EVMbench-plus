# P3 repository grounding: Securitize On-Off Ramp

Status: `resolved_for_on_off_ramp_only`

## Primary repository (admitted)

- URL: `https://github.com/securitize-io/bc-on-off-ramp-sc.git`
- Vulnerable commit: `a944bb11b106c13a5e43f8de01c9c01eeb5bb472`
- Root tree: `414c5718a9daee2dc3ffdc52c2d4b68ce3659809`
- Framework: Hardhat (TypeScript), Apache-2.0
- Submodules: none
- Detached checkout verified in isolated review clone

PDF summary table shows prefix `a944bb11b106...`; GitHub resolves that prefix
uniquely to the full SHA above. Fix commit hyperlinks in the PDF point at
`https://github.com/securitize-io/bc-on-off-ramp-sc/commit/...`, establishing
the organization and repository name.

## Secondary repository (not admitted)

- Name: `bc-securitize-bridge-sc`
- Host: Bitbucket `securitize_dev` (404 without credentials)
- Vulnerable prefix: `60b6ef00e8a8`
- Fix commit (from PDF links): `1da35cde31a53e7b2de56de0d313ebdcb80cbfa3`
- No public GitHub mirror with the audited tree was found

Per the grouping rule, bridge findings cannot share the on-off-ramp task key.

## Scope mapping

Report paths use `\bc-on-off-contracts\contracts\...`. The public repository
stores the same Solidity files under `contracts/...`. All listed on-off-ramp
files exist at the vulnerable commit. Bridge paths are out of this candidate.
