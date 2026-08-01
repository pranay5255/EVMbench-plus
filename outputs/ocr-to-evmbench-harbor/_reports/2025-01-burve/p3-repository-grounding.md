# P3 repository grounding: `2025-01-burve`

Status: passed.

The report's annotated GitHub link resolves to `itos-finance/Burve`. The
vulnerable commit is present and reviewed in a clean, detached, isolated clone
at `f0597768fee2d00c17429941f4721475e1ca5723`; its root tree is
`77fcc19230827f270cd36d9fbd7df947ec3749be`.

The report-named 19-contract scope maps to existing files under `src/`. All 16
recursive submodules were initialized at their pinned revisions. The separate
fix snapshot `e89ebff2c7daafc98e94c66e4273e4c366949c76` was used only to
corroborate report remediation and is not part of the task image.

Selected code anchors:

- C-01: `src/multi/Edge.sol` lines 402–478. All three implied-price branches
  place reserve division inside a shift count.
- C-02: `src/multi/facets/LiqFacet.sol` lines 62–88. `addedBalance` uses a
  delta, while `cumulativeValue` starts from the post-deposit balance.
- C-03: `src/multi/Diamond.sol` installs `diamondCut`; pinned Commons
  `DiamondCutFacet.sol` lines 18–29 leaves `AdminLib.validateLevel(3)`
  commented out.
- C-04: `src/Burve.sol` lines 193–211 transfers from a decoded payer without
  authenticating `msg.sender` as the pool.
- M-01: `src/Burve.sol` lines 120–188 and 218–232 expose mint/burn without
  bounds and derive island shares from execution-time `pool.slot0()`.

Post-audit commits independently corroborate C-01, C-02, C-04, and M-01. C-03
does not rely on a fix commit: the authorization omission is explicit in the
pinned dependency source.
