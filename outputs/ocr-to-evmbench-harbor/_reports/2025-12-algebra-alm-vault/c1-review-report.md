# C1 human review: `2025-12-algebra-alm-vault`

The pre-approval workflow is complete and stopped at the mandatory human gate.
No EVMBench admission, Harbor generation, registry publication, or agent/model
run has occurred.

## Approval-bound identity

- Candidate: `2025-12-algebra-alm-vault`
- Review-manifest SHA-256 (review-bundle digest):
  `2c000284d67d69a48f3d9f44f4181f5b47a23277ff55c08bd6bddf862648bb08`
- Repository: `https://github.com/cryptoalgebra/AlmVault.git`
- Vulnerable commit: `57d820afa1d58bf89073e668f5608942d90188c7`
- Task-key SHA-256:
  `b0a86f577e29a804775ae9046739ce20d4b79ebc2167c8889638b011c841047e`
- Mode/framework/policy: `detect` / Hardhat / `loss_of_assets`

Approval is valid only if it names the candidate, exact manifest digest, and
reviewer identity.

Suggested approval phrase:

```text
I approve candidate 2025-12-algebra-alm-vault at review-bundle digest
2c000284d67d69a48f3d9f44f4181f5b47a23277ff55c08bd6bddf862648bb08 for admission.
Reviewer: <identity>.
```

## Source evidence

| Item | Value |
|---|---|
| Rank | 17 (explicit out-of-order selection) |
| PDF SHA-256 | `810310a7d0bc20feb362250ebef10fd22946436fdd1dc998431be2a490819856` |
| OCR SHA-256 | `cebf3de80fc6909d3af0c82800c8ce86e77401726a1b29b2df46f266093f9525` |
| Pages | 35 / 35 |
| Report | MixBytes Algebra ALM — 19 Dec 2025 |

OCR is host-side discovery evidence. JSONL was not rewritten. PDF link
annotations supply the repository URLs; PDF text + live Git objects correct
OCR-garbled commit hex.

## Task-group resolution

The PDF scopes **two** public repositories:

1. `cryptoalgebra/AlmVault` (selected here)
2. `cryptoalgebra/plugins-monorepo` (separate task group; not admitted here)

Vulnerable vault snapshot is the **Initial Commit**
`57d820afa1d58bf89073e668f5608942d90188c7`, not re-audit
`d637339f968d67f175e8cb56ce3ae54a69bdefee` (which already contains the L-7 fix
`9f5f362a3723e9ec6fe8686fd30a22948653e1d8`).

## Selected findings

| Candidate | Report | Pages | Asset-loss root cause |
|---|---|---:|---|
| `H-01` | `L-7` | 23–24 | Donation inflation + floor division can mint 0 shares; attacker withdraws victim deposits |

All 18 report findings were dispositioned. Only L-7 qualifies under
`loss_of_assets` for this vault snapshot. Plugin findings and non-theft vault
findings are excluded (see `p4-finding-dispositions.md`).

## Validation result

| Check | Result |
|---|---|
| OCR schema/immutability | 35/35 records; source hash unchanged |
| PDF hash + page count | PASS |
| Repository resolution | Exact clean detached commit; 9 scope files; no submodules |
| Finding dispositions | 18/18; 1 selected |
| Evidence slices | Pages 6–7 and 23–24 byte-exact OCR rows |
| Offline baseline | Hardhat compile + **71/71** tests |
| Current structural validator | Passed; 0 errors/warnings |
| Pinned validator (`38957485…`) | Passed; 0 errors/warnings |
| No-cache image build | Passed; image `sha256:e2583186e2053a193f18b540118fa7de226d473781ec12050d61a3abdae5cc84` |
| Network-disabled image HEAD/clean/pdf-jsonl checks | PASS |
| Focused image leakage (audit/agent evidence) | PASS (0 hits) |
| Candidate Docker context leakage | PASS (dockerignore `**` + no COPY/ADD) |

Local-only C1 image size ≈ 4,136,290,809 bytes. No registry digest. Must not be
treated as admitted or published.

## Required reviewer judgments

1. Is splitting the PDF into vault-only vs plugin-only task groups correct, with
   this candidate limited to `cryptoalgebra/AlmVault`?
2. Is the vulnerable snapshot correctly the initial commit `57d820…` rather than
   re-audit `d637339…`?
3. Is selecting only L-7 under `loss_of_assets` (excluding L-6 CEI, L-5/L-14
   manager issues, L-10 transfer DoS, etc.) acceptable?
4. Is MIT SPDX on contracts sufficient despite null GitHub license metadata?
5. Is a single Low-severity but concrete theft finding sufficient for a detect
   task?

## Explicit non-actions until approval

- No `approved_for_admission` write
- No EVMBench admission / `audit_registry` mutation
- No Harbor task generation
- No registry image publish
- No agent/model smoke
- Canonical dirty `forestOfAudits` checkout untouched
- Selected-20 queue not updated to `created` until post-approval completion

## After approval

Resume only for this exact candidate and digest: admit → images by digest → one
Harbor task → Harbor 0.20.0 load → network-disabled no-model verifier replay →
final integrity → queue update marking Algebra created while keeping Benqi as
canonical next (unless separately directed).
