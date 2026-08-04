# Finding dispositions under `loss_of_assets`

| Report finding | Severity | Disposition | Reason |
|---|---:|---|---|
| 6.1 Inconsistent Price Conversion Logic Leads to Incorrect Oracle Prices | High | **Included as H-01** | The inverted conversion corrupts queue settlement rates. Source shows deposits mint shares by multiplication and redemptions release assets by division, producing a concrete transfer/loss path after an authorized oracle report is accepted. |
| 6.2 Off-chain price calculation can result in an infinite loop | High | Excluded | The report grounds keeper non-termination, stale prices, and denial of service. It says stale prices could be exploited but does not establish a concrete asset-transfer or permanent asset-loss sequence under the selected policy. |
| 6.3 Incorrect Natspec for CUSTOM_VERIFIER verification data | Info | Excluded | Documentation/encoding guidance defect; no asset-loss sequence. |
| 6.4 Incorrect natspec for ClaimableRequestExists error | Info | Excluded | Documentation defect; no asset-loss sequence. |
| 6.5 Use of abi.encodePacked with dynamic types could lead to storage slot collisions | Info | Excluded | Hypothetical state-collision risk, acknowledged by the client as inapplicable because contract names and instance names are static; no concrete loss sequence in the audited configuration. |

All five report findings are dispositioned. No broader-security exception was
requested or applied.
