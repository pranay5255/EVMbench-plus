# P5 build baseline: Securitize on-off-ramp

- Detached review HEAD: `a944bb11b106c13a5e43f8de01c9c01eeb5bb472`
- Framework: Hardhat (TypeScript), Apache-2.0
- Host Node: v22.22.2 used for install attempts
- `npm ci` fails: `@securitize/digital_securities@3.1.4` → HTTP 404 on
  registry.npmjs.org (resolved URL from package-lock). The checked-in upstream
  `.npmrc` auth token does not recover the package.
- Multiple contracts import interfaces from that package, including
  `contracts/on-ramp/SecuritizeOnRamp.sol` (H-01 surface).
- Agent Dockerfile strategy: **source pin only** (exact commit, no `npm ci`),
  so the agent can inspect vulnerable Solidity offline. Compile is not part of
  the image smoke until the package is recovered.
- `.dockerignore` is deny-all except Dockerfile; no host gold/OCR/PDF enters
  the build context.

## Upstream hygiene

Public tree includes `.npmrc` with an npm auth token. Do not copy a local clone
into the agent image; the Dockerfile fetches the pinned commit from GitHub.
