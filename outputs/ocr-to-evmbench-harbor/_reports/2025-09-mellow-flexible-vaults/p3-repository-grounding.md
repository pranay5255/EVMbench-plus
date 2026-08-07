# Repository grounding

The report names `mellow-finance/flexible-vaults`. A fresh disposable clone was
checked out at detached HEAD
`60c462d6b006b19790b07c009b7a48aa3bcb3e96`; its commit object, root tree,
parents, recursive submodule pins, clean status, and ancestry were verified.

The headline initial commit `69413d54...` is navigation evidence, not a usable
candidate snapshot for H-01: `src/oracles/OracleHelper.sol` does not exist
there. Embedded PDF links for the audited OracleHelper file and the two
OracleHelper findings resolve to `60c462d6...`. That commit contains all 75
Solidity paths in the PDF audited-files table, and its `src/**/*.sol` set has no
extra or missing path relative to the report. The selected snapshot is an
ancestor of final fix commit `72f689f9...`.

At the vulnerable snapshot:

- `OracleHelper.sol:7-16` defines `priceD18` as base-asset units per asset.
- `OracleHelper.sol:77-83` reads non-base redeem demand and divides it by the
  relative price.
- `OracleHelper.sol:87-104` uses the malformed demand in the base-price
  denominator.
- `OracleHelper.sol:113-117` propagates the base price to non-base assets.
- `DepositQueue.sol:140-151` and `:188-197` mint shares with
  `assets * priceD18`.
- `RedeemQueue.sol:227-240` releases assets with `shares / priceD18`.
- `Oracle.sol:103-120` is a role-gated submission path; `:184-224` validates
  and may mark reports suspicious before they affect queues.

The final commit changes the redeem-demand conversion to multiplication and is
used only as remediation evidence.
