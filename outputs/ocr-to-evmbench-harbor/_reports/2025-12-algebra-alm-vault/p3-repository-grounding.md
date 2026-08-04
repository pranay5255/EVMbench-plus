# P3 repository grounding — cryptoalgebra/AlmVault

## Resolved identity

| Field | Value |
|---|---|
| Canonical URL | `https://github.com/cryptoalgebra/AlmVault.git` |
| Vulnerable commit | `57d820afa1d58bf89073e668f5608942d90188c7` |
| Root tree | `df87262a3b75f1f95b2f20a78fceb280579b9838` |
| Parents | `66b2944672fe4e7d5a46b5703b41295f2360c6b3`, `fe4d9266a2c87656387e2adbc18ce24d1066246d` |
| Subject | Merge branch 'feature/farming-rewards' into integral-1.2.2 |
| Authored | 2025-11-10 12:52:10 +0300 |
| Framework | Hardhat / Solidity 0.8.20 (`viaIR`, optimizer runs 0) |
| Submodules | none |
| Public | yes |
| License | MIT (SPDX on contracts; GitHub API license null) |

## Why this commit (not the re-audit commit)

PDF Versions Log:

- `57d820…` — Initial Commit (ALM Vault)
- `d637339…` — Re-audit Commit (ALM Vault)

Client fix commits for vault findings (for example L-7
`9f5f362a3723e9ec6fe8686fd30a22948653e1d8`) are ancestors of `d637339…` and
descendants of `57d820…`. At `57d820…`, `MIN_SHARES = 1000` and deposit does not
revert on zero shares. At `d637339…`, the L-7 fix is already present. Therefore
the vulnerable snapshot for detect-mode gold is the **initial** commit.

## Sibling repository (not this candidate)

PDF also scopes `cryptoalgebra/plugins-monorepo` ALM plugin packages at initial
commit `6a5bcc44abfb90c3edb05bbea7efec233b5bd257` with re-audit commits
`facb3310…` and `9fc58be6…`. Those form a **different** task-group key and are
excluded from this candidate.

## Checkout verification

Isolated clone: `/tmp/algebra-alm-recovery/AlmVault`

```text
git cat-file -t 57d820afa1d58bf89073e668f5608942d90188c7  -> commit
git checkout --detach 57d820afa1d58bf89073e668f5608942d90188c7
git rev-parse HEAD = 57d820afa1d58bf89073e668f5608942d90188c7
git submodule status --recursive = (empty)
```

All nine vault scope paths from the PDF exist at that commit.

## Build baseline (host review clone, Node v20.19.6)

- `npm ci` — success
- `npx hardhat compile` — 85 Solidity files compiled
- `npx hardhat test` — **71 passing**
