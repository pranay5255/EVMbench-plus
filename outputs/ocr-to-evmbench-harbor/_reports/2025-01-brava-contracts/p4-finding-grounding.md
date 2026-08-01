# P4 finding grounding and dispositions: `2025-01-brava-contracts`

Status: passed with an explicit merge/split judgment. All 16 report findings
are dispositioned and no item remains unresolved.

| Report ID | Pages | Disposition | Code-grounded reason |
|---|---:|---|---|
| BRAV-01 | 8 | Exclude | Arbitrary role revocation can disable administration, but the report/code do not establish theft, destruction, or permanent asset loss from user-controlled Safes. |
| BRAV-02 | 9 | Include in H-01 | An unguarded Safe can call `setFeeTimestamp` directly, erase accrued time, then withdraw while transferring only a negligible post-reset fee. |
| BRAV-03 | 10 | Exclude | The stale pre-fee share balance makes Across withdrawal revert atomically; the report describes a zero-fee workaround and no asset transfer or destruction. |
| BRAV-04 | 11 | Merge into H-01 | Disabling the fee module is another symptom of the missing Safe guard. Alone it delays collection because ordinary deposit/withdraw paths still assess fees. |
| BRAV-05 | 12 | Split into H-01/H-02/H-03 | The report combines three mechanisms: arbitrary Safe calls, stale fee-free `exit` selectors, and generic receipt-token transfer. They require one merged boundary finding plus two independent selector-level findings. |
| BRAV-06 | 13 | Exclude | Fee collection can make a later Across deposit revert, but execution is atomic and does not consume or misdirect assets. |
| BRAV-07 | 14 | Exclude | A share/underlying denomination mismatch changes quantity, but redemption remains exchange-rate backed and the report does not establish value theft or destruction. |
| BRAV-08 | 15 | Exclude | A pre-existing receipt-token balance blocks fee initialization and causes an atomic supply revert; availability only. |
| BRAV-09 | 16 | Exclude | Excess ETH remains in the same user-owned Safe and is recoverable with an owner call. |
| BRAV-10 | 17 | Exclude | An already privileged fee proposer can delay a configuration update; no asset transfer or accounting corruption is established. |
| BRAV-11 | 18 | Exclude | A privileged executor can reuse an old proposal, but the report does not show the approved pool stealing or destroying user assets. |
| BRAV-12 | 19 | Exclude | The max-sentinel event amount can be wrong while transfer amount and recipient remain correct. |
| BRAV-13 | 20 | Exclude | A deposit above `maxDeposit` reverts atomically; compatibility/availability only. |
| BRAV-14 | 21 | Exclude | Possible third-party geo-restriction is a policy risk, not a concrete audited-contract asset-loss path. |
| BRAV-15 | 22 | Exclude | Role-grant limitations affect administration but do not establish an asset-loss sequence. |
| BRAV-16 | 23-24 | Exclude | The report groups stale code, repeated reads, typos, and comments as non-security miscellany. |

The three selected gold findings all lead to permanent loss of
asset-denominated fees to the configured fee recipient. Inclusion is based on
the executable loss path, not the report severity label.
