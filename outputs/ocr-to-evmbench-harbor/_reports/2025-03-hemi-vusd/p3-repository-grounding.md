# P3 repository grounding — Hemi Labs VUSD

Status: **PASS**

## Resolved vulnerable snapshot

- Repository:
  `https://github.com/hemilabs/vusd-stablecoin.git`
- Vulnerable commit:
  `54f9f235f26df813152b3d3235e7f4373ce473b6`
- Root tree:
  `f0214c72689158da00ff7d14be3d87008db4c57b`
- Commit subject:
  `Merge pull request #3 from patidarmanoj10/main`
- Commit authored:
  `2025-03-05T17:59:42+05:30`
- Checkout: detached, clean, isolated under `/tmp`
- Recursive submodules: none
- Tracked PDF/JSONL files: `0`

## Exact task identity

```text
hemilabs/vusd-stablecoin@54f9f235f26df813152b3d3235e7f4373ce473b6|contracts/|detect
```

SHA-256:
`9fcaf3e387f95a3c87e9c02ef235b20d88cfa2d6d7946a7157e47f8242832970`

The report scopes the repository tree at this exact commit. All selected
findings are in `contracts/`, so the audited task scope is recorded as
`contracts/`.

## Selected file evidence

| Path | Git blob | SHA-256 |
|---|---|---|
| `contracts/Treasury.sol` | `f584bdb296ec91d933a26389602f5df8b437a5bd` | `61c1e500084b96f0b4081ceb91a93524c78d58d7a760b34bea8bd49ac7a320e0` |
| `contracts/Minter.sol` | `c3571743f88cebbafbaf77779226666f509659ff` | `e3ca778b046d8298469b06814ec3221909c8ebdadb07a2207dc29985e85e17a2` |
| `contracts/Redeemer.sol` | `623899817620b09a8b2450746a3bdb1b8066bb82` | `db8b387edeb11dc8667c53196316c15e8baf796d7a450ea3dd6317fd44f26ae3` |

The report's function names and line-linked snippets match this snapshot.

## Fixed-state boundary

The immediate post-audit commit
`f3dec329d42c6e6b81ea61c3f4f4dd3340e976e2` changes `Minter._mint` to
calculate issuance from `balanceAfter - balanceBefore`, corroborating Bug #2.
It remains host-side evidence and is not used as the vulnerable task snapshot.
