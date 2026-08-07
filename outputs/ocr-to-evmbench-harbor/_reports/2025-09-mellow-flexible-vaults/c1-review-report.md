# C1 human review checkpoint: Mellow Flexible Vaults

Candidate `2025-09-mellow-flexible-vaults` is complete and remains
`in_review`. The exact approval object is
`c1-review-manifest.json` (6,143 bytes), SHA-256:

`7eba708f41fa4d90f56d47e170b8a624aafc84032bade60a88470929d740ee63`

## Identity

- PDF: `pdf_000135_167389a70b9f`, SHA-256
  `13a18507a8edf3db6e578788d853b76acc3935b1bac37ccc40b6c377f030ceab`
- OCR JSONL SHA-256:
  `2065910066cd953132dd4b184840cd20d5cd774db6c4edec3c7ce20d794c22e2`
- Repository: `https://github.com/mellow-finance/flexible-vaults.git`
- Vulnerable commit: `60c462d6b006b19790b07c009b7a48aa3bcb3e96`
- Root tree: `6a5951f96a4e85282fcd53fc3e93954b56e61e8a`
- Audited scope: all 75 Solidity files under `src/`
- Mode/policy: `detect` / `loss_of_assets`

The selected commit is an intermediate report-linked snapshot. The headline
initial commit lacks `OracleHelper.sol`; the PDF's audited-file and finding
links point to `60c462d6...`, which is between the headline initial and final
fix commits.

## Selected finding

H-01 is report finding 6.1: the helper divides non-base redeem demand by its
relative price instead of multiplying it. This corrupts shares-per-asset oracle
prices. Once an authorized helper-derived report is accepted, deposit queues
mint shares using multiplication and redeem queues release assets using
division, so users settle at an incorrect rate and one side loses value.

Finding 6.2 is excluded because its grounded impact is stale-price/keeper
denial of service rather than a concrete loss sequence. The three informational
findings are documentation or inapplicable/hypothetical issues. All five report
findings are explicitly dispositioned.

## Validation result

OCR schema/order/completeness, PDF review, exact Git object/tree/submodules,
75-file scope equality, loss-of-assets semantics, source build, 19/19 focused
OracleHelper unit tests, the full local unit suite, byte-exact evidence slices,
gold/finding equality, live structural validation, skill-pinned structural
validation, and Docker-context leakage checks all passed.

No model smoke was run. The integration suite was not replayed because it
requires `ETH_RPC`. No candidate image was built before approval. The exact
commit also has inconsistent license metadata: BUSL-1.1 source/README markers,
no standalone license file, and `UNLICENSED` in `package.json`.

## Required approval

Admission requires an explicit approval naming:

1. candidate `2025-09-mellow-flexible-vaults`;
2. digest `7eba708f41fa4d90f56d47e170b8a624aafc84032bade60a88470929d740ee63`;
3. reviewer identity.

Until then, `human_approved` remains false, no EVMBench admission or image is
created, no Harbor task is generated, and no agent/model run occurs.
