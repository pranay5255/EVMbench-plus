# Finding grounding and dispositions — VII Finance

| Report item | Pages | Disposition | Code-grounded reason |
|---|---:|---|---|
| C-1 | 6–13 | Split/merged | Composite liquidation chain built from H-1, H-2, and zero-balance enrollment; no additional vulnerable operation, so its asset-loss mechanisms are scored through the underlying root causes. |
| H-1 | 14–20 | Include as H-01 | Persistent `tokensOwed` credits remain after payout and can drain fees reserved for other holders. |
| H-2 | 21–23 | Include as H-02 | `normalizedToFull` uses global supply instead of sender balance, causing excess collateral seizure or liquidation reverts/bad debt. |
| M-1 | 24–25 | Include as H-03 | Full unwrap transfers the NFT without settling V4 fee assets, making them unreachable. |
| M-2 | 25–29 | Include as H-04 | Floor rounding lets a valuable residual position transfer zero units to a partial liquidator. |
| L-1 | 30–32 | Exclude | The report says no clear material attack was found, deferred checks still protect undercollateralized accounts, and recursive unwraps appear unprofitable. |
| L-2 | 33 | Exclude/merge | Enrollment without ownership is observable, but its asset-loss path relies on H-2 and is eliminated by the same H-2 normalization fix; separate scoring would duplicate a root cause. |
| L-3 | 33–35 | Exclude | The recoverable NFT is an empty zero-liquidity position; no retained asset value or theft path is established. |
| I-1 | 36 | Exclude | Caller-supplied malformed data causes a revert but does not move, destroy, or strand assets. |
| I-2 | 36 | Exclude | Duplicate import only; code quality. |

The selected four findings each require a different corrective code change and
each has a direct or indirect loss of user, liquidator, or vault assets.
