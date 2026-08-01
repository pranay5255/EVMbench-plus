# GitHub CLI code matching: Benqi Governance

Status: `matched_report_text_only_exact_snapshot_still_blocked`

Using `gh api` in the CLI, distinctive identifiers and PoC names from the
checksum-verified PDF/OCR were searched in GitHub's code index, including a
fork-inclusive pass.

## Match result

| OCR/PDF anchor | Report finding | Report-named source area | GitHub match |
|---|---|---|---|
| `_collectVotes`, `epochGaugeVotes(0, gaugeAddress)`, `enableUpdateVotingPowerHook` | L-01 | `DistributionManager.sol`, `DistributionManagerSetup.sol` | Audit Markdown only |
| `calculateMarketBudgetUsed`, `hasRegisteredSupplyGauge`, `hasRegisteredBorrowGauge` | L-05 | `BenqiCoreModule.sol`, `DistributionManager.sol` | Audit Markdown only |
| `_validateCanDistribute`, `NoModulesConfigured`, `VotingStillActive`, `testPoC_bufferWindowSkipsEpoch` | L-07 | `DistributionManager.sol`, `Clock.sol`, report PoC test | Audit Markdown only |
| `calculateSpeeds`, `hasRegisteredSupplyGauge`, `test_deactivateSupplyGauge_usesExistingSpeed` | L-08 | `BenqiCoreModule.sol`, report PoC test | Audit Markdown only |
| `rewardControllerToModule`, `_activeRewardControllers`, `getGaugeByRewardController`, `ZeroTotalVotes` | L-11 | `DistributionManager.sol`, `GaugeRegistrar.sol`, `UnifiedBudgetAllocator.sol` | Audit Markdown only |

The official indexed match is
[`Cyfrin/cyfrin-audit-reports`](https://github.com/Cyfrin/cyfrin-audit-reports/blob/e58c7c874afc2feb45828079312669e9be6e3f60/reports_md/2025-11-10-cyfrin-benqi-governance-v2.0.md),
blob `623e91bd719872b8858305d30ad7fff69be95ef2`. The same text also appears in
Solodit and several audit-dataset copies. These matches confirm that the OCR
snippets correspond to the public report, but they do not recover the audited
Solidity tree.

All Solidity-filtered searches for the distinctive contract names and
identifiers returned zero results. The fork-inclusive non-language searches
found only report forks. `getAllRegisteredGaugeDetails` additionally matched
TypeScript ABI/hooks in forks of [`aragon/app`](https://github.com/aragon/app),
which corroborates the frontend interface but is not contract source. A generic
emission-token error string matched an unrelated BENQI
`MultiRewardDistributor.sol`; it is outside this repository and audited scope.

## Asset result

The same CLI route enumerated 210 visible Aragon repositories, 1,014 releases,
232 release assets, and 5,389 Actions artifacts. There was no exact audited
commit or audited-contract asset. All 37 Benqi-tagged artifacts were expired
`aragon/app` Next.js builds; a download probe returned `410 Gone`.

The package endpoint remains ambiguous because the current token lacks the
`read:packages` scope. That limitation is not treated as proof that packages do
not exist.

## Gate consequence

The code can be matched from OCR/PDF to the audit report and its report-named
paths, but not to a verifiable checkout of
`ded42b671f112eef318482a8c9f10329d0aeef65`. Report snippets, PoCs, frontend
ABIs, and reconstructed files are navigation evidence only. Candidate creation
therefore remains prohibited by the exact-snapshot gate.

The complete endpoint counts, query strings, result classes, and snippet
crosswalk are recorded in `p3r3-gh-api-asset-and-code-recovery.json`.
