# Foundry on-chain simulation: Benqi Governance

Status: `live_calls_simulated_exact_snapshot_still_blocked`

Foundry `v1.7.1` was downloaded from the official `foundry-rs/foundry`
release asset with `gh api`. The archive SHA-256 exactly matches GitHub's
published asset digest. It was staged under `/tmp`; nothing was installed into
the workspace.

## Read-only result

`cast` queried Avalanche C-Chain (`43114`) without broadcasting a transaction.
The observed live proxy is `0xe3522b2828fd106e648b310b9c37909c261bba8d`.
Its EIP-1967 implementation slot changes from zero at block `73974527` to
`0x24591406F4090C2Bd5B35913e8E4c8cC415d1f51` at block `73974528`.

At block `73974570`, a historical `cast call` from the DAO address simulated:

```text
registerGauge(
  0x1D0e6c24611fDAeF8eDAab57E2016e3819d6f78B,
  1,
  0xB0A8acBE3432D75dF7D3992de2a8560924544595,
  "ipfs://simulation-only"
)
```

The read-only call succeeded and returned
`0x4946845D2D276D003ddFDdd4558419812aC1Fdfd`. This is an `eth_call` result:
zero transactions were broadcast and no state was persisted.

Foundry also decoded the three gauge tuples registered in that block and the
successful transaction
`0x29c174ad444fbdcec2890a94d0ce832fb1654b8440850bcd4ba01f236c1348cd`.
The complete addresses and call inputs are preserved in
`p3r4-foundry-onchain-simulation.json`.

## Why this does not unlock the candidate

The first observed registration is dated `2025-12-18`, after the
`2025-11-10` audit. More decisively, the OCR/PDF names the singular getter
`getGaugeByRewardController(address)`, which reverts with empty data on the
live runtime. Foundry resolves a different plural function,
`getGaugesByRewardController(address)`, which returns all three gauges.

That ABI mismatch is positive evidence that the live deployment materially
differs from the audited code. The implementation is not verified, its IPFS
metadata was unavailable, and a full-runtime search in Blockscout's Ethereum
Bytecode Database returned zero Eth Bytecode DB, Sourcify, and Alliance source
matches.

The simulation corroborates the later deployment's contract domain and shows
that its call path is executable. It cannot authenticate the vulnerable Git
object `ded42b671f112eef318482a8c9f10329d0aeef65`. The exact-snapshot gate
therefore remains failed closed, and no candidate or Harbor task was created.
