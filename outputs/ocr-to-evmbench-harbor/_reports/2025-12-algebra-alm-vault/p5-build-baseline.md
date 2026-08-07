# P5 build baseline — AlmVault@57d820a

Host review clone: `/tmp/algebra-alm-recovery/AlmVault`  
Node: v20.19.6 (host). Base image expects Node v22.22.3.

| Step | Result |
|---|---|
| `npm ci` | PASS |
| `npx hardhat compile` | PASS — 85 Solidity files |
| `npx hardhat test` | PASS — **71** tests |
| Submodules | none |
| Dirty tracked files after build | none (artifacts/cache/types/node_modules gitignored) |

Warnings only: local variable shadowing `currentTick` in `AlgebraVault.sol`.
