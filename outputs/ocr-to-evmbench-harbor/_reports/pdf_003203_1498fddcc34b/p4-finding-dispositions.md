# Initia finding dispositions

No report finding is included. The exact code snapshot is a React/TypeScript
frontend rather than an EVMBench smart-contract target, and all Router API
findings lack code in the sole audited commit. The table records the additional
finding-level reason so the framework rejection does not hide semantic review.

| ID | Pages | Code at audited SHA | Concrete asset-loss assessment | Disposition |
|---|---:|---|---|---|
| M-01 | 10–11 | Router API absent | Open proxy/SSRF and header forwarding; no report-grounded asset-loss sequence | Exclude: ungrounded component and no concrete asset loss |
| M-02 | 11–13 | Widget image paths present | `<img>` rendering of an SVG/data URI does not by itself establish script execution; phishing/spoofing is generic | Exclude: overclaimed mechanism; merge cluster M-05/L-14/L-22/L-23 if ever reconsidered |
| M-03 | 13–15 | `packages/widget-react/src/data/signer.ts:172–204` | A chain-only client cache can retain Wallet A's signer after the UI switches to Wallet B, causing an unintended transaction from A and direct asset loss | Exclude only because it is an off-chain frontend bug outside the EVMBench smart-contract target; candidate for a separately authorized frontend benchmark |
| M-04 | 15–18 | `ExplorerLink.tsx:17–37` and `ManageChainsItem.tsx:9–50` | Attacker-controlled registry URLs can use `javascript:` and execute after a click; the report does not establish a distinct transaction/fund-loss sequence | Exclude: frontend-only and asset-loss path not concrete enough |
| M-05 | 18–19 | `Image.tsx:12–35` | The report's `data:text/html` proxy/`<img>` PoC does not establish browser script execution; overlaps M-02 | Exclude: invalid or incomplete exploit mechanism |
| L-01 | 20 | `FooterWithErc20Approval.tsx` present | Partial approvals and failed-transaction gas; no demonstrated attacker-controlled loss path | Exclude: gas/failure handling only |
| L-02 | 20–21 | `BridgeFields.tsx:131–151` present | Submission with insufficient fees can fail and waste gas | Exclude: gas-only/user error |
| L-03 | 21 | Router API/deployment absent | Generic container hardening | Exclude: ungrounded and conditional infrastructure risk |
| L-04 | 22 | Router API/chart absent | Generic cluster hardening/availability | Exclude: ungrounded and no concrete asset loss |
| L-05 | 22–23 | LayerZero function and constants absent | Report claims possible bridge fund lock, but the cited snippet cannot be found in the audited tree or a public matching repository | Exclude: asset-loss claim cannot be code-grounded |
| L-06 | 23 | Widget logging exists | Information disclosure claim is nonspecific | Exclude: no concrete asset loss |
| L-07 | 23–24 | External links present | Reverse tabnabbing enables generic phishing only | Exclude: no concrete code-to-asset-loss sequence |
| L-08 | 24–25 | Server/deployment target absent | Generic browser headers | Exclude: ungrounded and no concrete asset loss |
| L-09 | 25 | Router API absent | Permissive CORS | Exclude: ungrounded and no concrete asset loss |
| L-10 | 25–26 | Router API absent | Technology disclosure | Exclude: informational only |
| L-11 | 26–27 | Router API `/nft` code absent | ORDERED-channel closure is availability impact | Exclude: ungrounded and availability-only |
| L-12 | 27–28 | Router API absent | Unhandled promise errors | Exclude: ungrounded and availability-only |
| L-13 | 28 | Router API absent | Incorrect HTTP exception semantics | Exclude: ungrounded and no asset loss |
| L-14 | 29 | `WithNormalizedNft.tsx` present | Untrusted metadata feeds the shared image cluster | Exclude: duplicate symptom of M-02/M-05; exploit mechanism and asset loss not established |
| L-15 | 29–31 | Router API absent | A compromised/malformed route API could be economically dangerous, but the exact implementation is missing | Exclude: potentially relevant root cause cannot be grounded |
| L-16 | 31 | Endpoint infrastructure absent | Legacy TLS is an operational configuration issue | Exclude: ungrounded and no snapshot-local root cause |
| L-17 | 31–32 | Router API absent | Request hang/resource exhaustion | Exclude: availability-only and ungrounded |
| L-18 | 32–34 | `ky` clients present | UI requests can hang | Exclude: availability-only |
| L-19 | 34 | Form refinement present | Invalid input can crash a form | Exclude: availability/UI only |
| L-20 | 34–36 | Encoding function present | The report explicitly says there is no immediate security risk | Exclude: defense in depth only |
| L-21 | 36–37 | `data/tx.ts:195–225` present | One-block confirmation can misreport a reorged transaction, but the report gives no downstream release or asset-loss sequence and the client is not a smart contract | Exclude: frontend-only and no concrete loss path |
| L-22 | 37–38 | `CollectionDetails.tsx` present | React escapes rendered strings; the report relies on a hypothetical future `dangerouslySetInnerHTML` change | Exclude: no current vulnerability |
| L-23 | 38 | `BridgeAccount.tsx:1–33` present | Wallet image spoofing/proxy abuse; overlaps shared image cluster | Exclude: no established XSS or concrete asset loss |

## Distinct root causes retained for possible non-EVMBench follow-up

Only M-03 is both code-grounded and backed by a concrete unintended-asset-use
sequence. M-04 is code-grounded but needs a stronger asset-loss chain. Neither
may be admitted under the current EVMBench smart-contract instruction contract
without explicit authorization to change benchmark scope.
