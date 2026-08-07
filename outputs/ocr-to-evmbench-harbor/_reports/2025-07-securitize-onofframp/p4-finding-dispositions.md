# P4 finding dispositions: Securitize On-Off Ramp / Bridge

Policy: `loss_of_assets`
Primary task group: `securitize-io/bc-on-off-ramp-sc@a944bb11b106c13a5e43f8de01c9c01eeb5bb472`

The PDF covers two repositories. Only the public on-off-ramp snapshot is admitted
in candidate `2025-07-securitize-onofframp`. Bridge findings are dispositioned as
held for a separate task group pending an exact public snapshot.

| Report ID | Pages | Repo group | PDF-layer impact | Disposition |
|---|---:|---|---|---|
| C-1 | 10–11 | on-off-ramp | Replay of EIP-712 approvals double-debits investor liquidity and re-delivers DS tokens | **Selected → H-01** |
| M-1 | 12 | on-off-ramp | Unnecessary reverts from fee-blind `minOutputAmount` | Exclude: availability/UX, no concrete asset-loss path |
| M-2 | 12–13 | bridge | AA wallets receive bridged DS tokens at wrong destination address | Hold: concrete permanent loss claim, but bridge snapshot unavailable |
| M-3 | 13–14 | bridge | Pausing receiver functions permanently sticks in-flight funds | Hold: asset lock claim, bridge snapshot unavailable |
| M-4 | 14–15 | on-off-ramp | `availableLiquidity` assumes 1:1 collateral→liquidity | Exclude under loss_of_assets: report impact is incorrect liquidity info / failed txs |
| L-1 | 15–16 | bridge | Admin can set too-low gas limit, failing deliveries | Exclude / bridge: admin config + availability |
| L-2 | 16 | on-off-ramp | Missing liquidityToken match on initialize | Exclude: privileged misconfiguration during setup |
| L-3 | 16–17 | on-off-ramp | `liquidityProviderWallet` unset at init | Exclude: temporary failed redemptions until admin sets wallet |
| L-4 | 17 | on-off-ramp | Missing storage gaps | Exclude: upgrade-safety hygiene without concrete loss path |
| L-5 | 17–18 | both/base | Single-step ownership transfer | Exclude: privileged ownership hygiene |
| L-6 | 18–19 | on-off-ramp | `msg.sender` vs `_msgSender()` | Exclude: meta-tx support gap without demonstrated loss |
| L-7 | 19–20 | bridge | Immutable `whChainId` | Exclude: design/closed |
| L-8 | 20 | bridge | Hardcoded refund address | Exclude / bridge: refund configurability |
| L-9 | 20–22 | bridge | Unofficial wormhole npm package | Exclude / bridge: supply-chain maintenance risk without grounded public tree |
| I-1 | 22–23 | on-off-ramp | Misleading comments | Exclude: docs |
| I-2 | 23 | on-off-ramp | Unnecessary override keywords | Exclude: style |
| I-3 | 23–24 | on-off-ramp | Wrong event type on swap | Exclude: telemetry |
| I-4 | 24–25 | on-off-ramp | Missing `_disableInitializers` | Exclude: implementation init risk without proxy-path asset loss |
| I-5 | 25 | on-off-ramp | Weak country-code checks | Exclude: compliance format |
| I-6 | 25–26 | on-off-ramp | Confusing fee variable names | Exclude: naming |
| I-7 | 26 | on-off-ramp | Unused modifier parameter | Exclude: style |
| I-8 | 26–27 | on-off-ramp | Complex decimal math | Exclude: clarity/gas |
| I-9 | 27 | bridge | Unused CCTP library | Exclude: dead code |
| I-10 | 27 | on-off-ramp | Zero minOutput in nested collateral redeem | Exclude: acknowledged future-integration concern; outer path has slippage |

## Selection result

Selected findings: **H-01** (report C-1 only).

Bridge findings M-2/M-3 remain navigation targets for a future
`bc-securitize-bridge-sc` candidate if/when the exact audited Git object is
available.
