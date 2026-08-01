# P3 repository grounding: `2025-06-recall-contracts`

The report's clickable scope links resolve to two different public repositories.
This candidate uses only the Solidity group:

- repository: `https://github.com/recallnet/contracts.git`
- audited vulnerable commit: `5a6710409a90944ceb3ff4d8ad9edea1b00557c3`
- framework: Foundry
- first-party scope: `src/**`, `script/**`, `test/**`
- exclusion: vendored third-party `lib/**`

The clean detached checkout contains the selected report snippet at
`src/token/ValidatorRewarder.sol:82-88`. `notifyValidClaim` is guarded by that
modifier and the unexecuted body at lines 120-165 performs the validator reward
mint or transfer. The report's parallel `ValidatorGater` symptom is excluded
from gold because its power-range bypass has no report-grounded asset-loss
sequence.

The report's Rust findings resolve to `recallnet/ipc` at full commit
`d08b2794743a9013502950292934fb98b0341c79` and are excluded from this task.
That historical checkout also has two SSH-only `hokunet/*` submodules, so it
does not satisfy the reproducible-submodule gate for a separate IPC candidate
without additional access or an exact public mirror.

PR #57 and commit `b5f6ef783bc28859b0caaa037d56a7298ee6d076`
corroborate the finding by replacing the rewarder's silent return with a
`ContractNotActive()` revert. No fix commit or post-audit history is used as
the vulnerable snapshot.
