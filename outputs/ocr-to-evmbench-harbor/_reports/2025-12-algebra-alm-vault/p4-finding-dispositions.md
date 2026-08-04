# P4 finding dispositions — Algebra ALM

Policy: `loss_of_assets` (canonical; no broader_security authorization).

Vulnerable vault snapshot: `cryptoalgebra/AlmVault@57d820afa1d58bf89073e668f5608942d90188c7`.

| Report ID | Title | Pages | Repo | Disposition | Reason |
|---|---|---:|---|---|---|
| M-1 | Missing Rebalance Bookkeeping Updates After Successful Rebalance | 13 | plugins-monorepo | **excluded** | Different repository / task-group key; rebalance throttling distortion without proven direct asset theft in this candidate |
| L-1 | Inaccurate Percentage Calculations Due to Unclaimed Fees | 14–16 | plugins-monorepo | **excluded** | Other repository; suboptimal ranges, acknowledged |
| L-2 | Unnecessary Gap Between Base and Limit Positions | ~15–16 | plugins-monorepo | **excluded** | Other repository; acknowledged design |
| L-3 | Hardcoded Minimum Gas Threshold | 18 | plugins-monorepo | **excluded** | Other repository; operational flexibility |
| L-4 | Incorrect State Return When Rebalance Not Needed | 19 | plugins-monorepo | **excluded** | Other repository; monitoring-only state bug per report |
| L-5 | Missing Whitelist Check for Reward Tokens in getReward() | 20–21 | AlmVault | **excluded** | Pollutes user bookkeeping for non-whitelisted tokens; no demonstrated theft of staked/reward assets |
| L-6 | Checks-Effects-Interactions Pattern Violation in _getReward() | 22 | AlmVault | **excluded** | CEI / reentrancy hardening; project threat model is standard ERC-20 without transfer hooks; no concrete asset-loss PoC under that model |
| L-7 | Rounding Error Allows Theft of User Deposits via Donation Attack | 23–24 | AlmVault | **selected → H-01** | Direct donation inflation + floor division mints 0 shares; attacker withdraws victim deposits |
| L-8 | Risk Parameter Setters Lack Cross-Validation | 25 | AlmVault | **excluded** | Admin misconfiguration can DoS rebalance; trusted-actor / no unprivileged theft path |
| L-9 | Typo in Comment | 26 | AlmVault | **excluded** | Documentation only |
| L-10 | Unsafe ETH Transfer Using transfer() Instead of call() | 27 | AlmVault | **excluded** | Withdrawal gas stipend availability issue for complex receivers; not a theft path |
| L-11 | Unused Code | 28 | AlmVault | **excluded** | Dead code |
| L-12 | Precision Loss in _removeDecimals() for extreme pairs | 29 | plugins-monorepo | **excluded** | Other repository; acknowledged edge-case unusability |
| L-13 | Incorrect Tick Rounding for Negative Exact Multiples | 30 | plugins-monorepo | **excluded** | Other repository; acknowledged minimal impact |
| L-14 | Missing Validation Allows Staking Token as Reward Token | 31 | AlmVault | **excluded** | Manager misconfiguration; trusted actor |
| L-15 | Quadratic Time Complexity in getReward() | 32 | AlmVault | **excluded** | Gas / availability cost growth only |
| L-16 | Unsafe approve() Usage in Constructor | 33 | AlmVault | **excluded** | Deployment compatibility with non-standard approvals; not runtime theft |
| L-17 | Missing Tick Bounds Validation in Range Calculations | 34 | plugins-monorepo | **excluded** | Other repository; acknowledged |

## Selected set

- `H-01` ← report `L-7` only.

## Notes

- Severity labels alone did not drive inclusion; L-7 is Low but has an explicit
  theft sequence verified in code.
- Deposit-guard slippage reduces practical likelihood; the vault function itself
  still implements the vulnerable mint path at the pinned commit.
