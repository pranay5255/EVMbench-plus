# P3 repository grounding: `2025-01-brava-contracts`

Status: passed.

The PDF's repository hyperlink resolves to
`https://github.com/brava-labs/brava-contracts`. Its vulnerable hyperlink
resolves to commit `655613454d3c6264096457adeb387b965fefc3c6`, which was
materialized in a fresh, detached, clean review clone. The root tree is
`adc6756be8d1c213aa1ed0e40532654932776d6d`; the `contracts` tree is
`ef5317418e5ccfcc79ead0745dfed72eb4c0d9d0`.

The PDF scope maps to `contracts/actions/**`, `contracts/auth/**`, and
`contracts/SequenceExecutor.sol`, containing 37 tracked files. The repository
uses Hardhat with npm, a committed lockfile, and Solidity 0.8.28. It has no Git
submodules. The fixed report commit
`29d4211f732e745a926209dc1cc915562a8c0b74` is a descendant of the vulnerable
commit and was kept outside the candidate image.

The vulnerable code directly corroborates all selected mechanisms:

- `AdminVault.sol:291-294` lets any caller reset its own fee timestamp.
- `SequenceExecutor.sol:65-67` delegatecalls arbitrary user-supplied calldata
  into a registered action.
- the Aave, Compound V2, ERC-4626, and Clearpool withdrawal actions expose
  `exit` entry points that omit `_processFee`;
- `SendToken.sol:27-54` transfers an owner-selected token without fee
  settlement.

Fix-history commits were used only as corroboration. The agent snapshot is a
depth-one fetch of the vulnerable commit, has one reachable commit, and
contains none of the fixed or post-audit commit objects.
