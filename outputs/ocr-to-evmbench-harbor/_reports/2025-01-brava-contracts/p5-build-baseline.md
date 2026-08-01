# P5 build and test baseline: `2025-01-brava-contracts`

Status: build passed; upstream fork-dependent tests disclosed as non-runnable
offline.

The exact detached vulnerable checkout uses Hardhat, npm, and Solidity 0.8.28.
On the host review clone, `npm ci` installed 1,027 packages and a forced
Hardhat compile produced 92 Solidity compilations and 172 artifact JSON files.
The host tool versions were Node v20.19.6 and npm 11.11.0.

The final agent image was rebuilt with `--no-cache`. Its base supplies Node
v22.22.3 and npm 10.9.8; `npm ci` again installed 1,027 packages and the build
compiled 92 Solidity files. A fresh `hardhat compile --force` under
`docker run --network none` also compiled all 92 files and left the audited Git
worktree clean. The Tenderly plugin logs an expected failed request to
`api.tenderly.co` under network isolation but Hardhat exits successfully.

The unmodified test suite requires a Tenderly mainnet-fork URL constructed
from `TENDERLY_API_KEY`. A bounded no-network run reached all 18 suites but
executed no tests: every suite failed in `before all` while resolving
`mainnet.gateway.tenderly.co` (0 passing, 18 hook failures). This is an
environment/reproducibility disclosure, not semantic validation of the gold;
no finding-specific tests were added.

`npm audit` reports 76 upstream dependency vulnerabilities: 12 low, 14
moderate, 42 high, and 8 critical. Dependencies were not modified because the
candidate must preserve the audited lockfile snapshot.
