# P5 build baseline — Lido v3

Status: **PASS**

## Pinned toolchain

- Base image:
  `pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0`
- Base image config:
  `sha256:fc20d776501708f9236e87b0e853d03f66d3b75af41a9ab1d1aad2c8b2c72fb9`
- Platform: `linux/amd64`
- Node: `v22.15.0`, exactly matching `.nvmrc`
- Node archive SHA-256:
  `dafe2e8f82cb97de1bd10db9e2ec4c07bbf53389b0799b1e095a918951e78fd4`
- Yarn: `4.9.2`, from `packageManager`
- Install: `corepack yarn install --immutable`

## Canonical repository checks

- `corepack yarn compile`: PASS
  - 408 Solidity files compiled
  - 1,266 project typings generated
- `corepack yarn test`: PASS
  - 2,555 passing
  - 0 failing
  - 19 pending

Node 22.22.3, which is present in the base image, triggers an upstream
parallel TypeScript-loader error after 2,265 passing tests. Re-running under
the repository-pinned Node 22.15.0 eliminates the error.

The full `forge build` is not the repository's canonical compile command and
hits an upstream Solidity stack-too-deep compiler error under Forge 1.3.6.
The candidate is therefore correctly classified as `framework: hardhat` and
uses the project's own `compile` and `test` scripts.

## Candidate image

- Local tag: `evmbench-lido-v3-core:c1`
- Image/config digest:
  `sha256:5b9ba64cb56749554da391939e53e29ce4d7c1663fa0fa981b144ff4e144e416`
- Platform: `linux/amd64`
- Size: `5,282,888,597` bytes
- Network-disabled forced Hardhat compile: PASS
- Agent-visible Git HEAD: vulnerable commit exactly
- Agent-visible Git commit count: `1`
- Leakage scan: PASS
