# Initia pre-candidate gate failure

Result: **fail closed at Gate 3; no EVMBench candidate was created**.

## Passed evidence gates

- The immutable OCR JSONL has 38 ordered records covering exactly pages 1–38.
  All 1,995 recorded global and per-record checks passed, and its before/after
  SHA-256 is
  `7c62a967214341879f7c01a853b12efa4b307410ef85efaa14e139ff1793c65c`.
- The original PDF is present, has 38 physical pages, and matches the recorded
  SHA-256
  `67d7fbfadc21cbf638f7114989fde983e16c002e336bc34c6c8ef0f52c59adc0`.
- The report's vulnerable commit
  `c7c7fc23a5d65cafbd8d748711a607abf695052a` is fetchable and was checked out
  cleanly and detached from the public successor repository
  `https://github.com/initia-labs/interwovenkit.git`.
- The checkout tree is
  `a342e9402d5e41debcd1de0851bf1c234420b251` and has no submodules.

## Failed required invariants

1. **The target is not an EVMBench smart-contract codebase.** The exact tree is
   a pnpm/Vite/Vitest React SDK containing TypeScript, TSX, and CSS. It has zero
   Solidity files and no Foundry, Hardhat, or Truffle configuration. EVMBench's
   detect instruction explicitly asks the agent to audit provided smart
   contracts, so silently packaging this frontend would change the benchmark
   contract.
2. **The report spans an unresolved second codebase.** The PDF says the scope
   includes Widget and Router API. The audited SHA contains the Widget paths but
   none of the `router-api/...` paths used by M-01, L-03–L-05, L-08–L-13,
   L-15–L-17. No second repository or audited commit is identified. The
   LayerZero fund-lock snippet is also absent from the exact tree.
3. **Zero findings survive the current benchmark eligibility boundary.** M-03
   is a credible frontend signer-cache asset-loss issue, but it is not a smart
   contract vulnerability. Treating it as one requires explicit authorization
   for a new off-chain/frontend benchmark scope, not an inference during this
   workflow.

## Prohibited downstream state

- Candidate ID: none.
- Review-bundle digest: none.
- Human approval state: not created.
- Canonical EVMBench admission: not attempted.
- Agent/verifier image build or publication: not attempted.
- Harbor task generation/load/replay: not attempted.
- Model/agent smoke: not attempted.
- Canonical `forestOfAudits` checkout: untouched.

The missing authority/evidence can be resolved only by either selecting a
different report with a smart-contract snapshot or explicitly defining and
approving a separate frontend/off-chain benchmark contract. Supplying a Router
API repository alone would not cure the Widget target's EVMBench framework
mismatch.
