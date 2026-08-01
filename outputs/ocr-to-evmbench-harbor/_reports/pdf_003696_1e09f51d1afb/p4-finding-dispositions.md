# EigenDA finding dispositions before candidate creation

No finding is selected. Every item was checked against the report and exact
vulnerable code. The table distinguishes a real defect from EVMBench's much
stricter requirement: a concrete direct or indirect loss of user or protocol
assets. A crash, timeout, retry, malformed response, diagnostic leak, or
configuration hardening concern does not qualify by itself.

| ID | Pages | Severity | Exact-code assessment | Disposition |
|---|---:|---|---|---|
| EDA-01 | 8–9 | Medium | `writeJSON` uses the content-type value as the header key (`handlers_misc.go:108–123`). The result is an incorrect HTTP header, while the JSON body and state transition are unchanged. | Exclude: API interoperability/correctness; no asset transfer, accounting error, or lock. |
| EDA-02 | 10–11 | Low | `RetrieveBlobChunks` blocks on one channel result per operator without selecting on context cancellation (`retrieval_client.go:181–217`). | Exclude: request latency/goroutine cleanup and availability only. |
| EDA-03 | 12–13 | Low | `GetChunks` opens a gRPC connection and never closes it (`node_client.go:79–157`). Repetition can exhaust file descriptors. | Exclude: resource exhaustion/availability only. |
| EDA-04 | 14–15 | Low | The deferred cleanup dereferences `conn` before checking the constructor error (`validator_grpc_manager.go:73–86`). A failed dial can panic. | Exclude: process crash/availability only. |
| EDA-05 | 16 | Low | The generic commitment route accepts an unbounded hex payload path (`routing.go:45–59`), enabling memory pressure. | Exclude: denial of service only; the report supplies no permanent asset lock. |
| EDA-06 | 17–18 | Low | `reservationWindow == 0` reaches integer division in `getOrRefreshRelativePeriodRecord` (`accountant.go:187–201`). `SetPaymentState` accepts the zero value (`accountant.go:210–220`); the cited on-chain setter is `onlyOwner` (`PaymentVault.sol:91–94`) and lies outside the strict report scope. | Exclude: client panic/dispersal availability. No mischarge or unauthorized movement of funds is demonstrated. |
| EDA-07 | 19 | Low | `GetChunks` has no default branch for a future/unknown encoding enum (`node_client.go:121–150`), leaving a nil frame or downstream error/panic. | Exclude: retrieval correctness/availability; no acceptance of uncommitted blob data is established. |
| EDA-08 | 20–21 | Low | A decoded keccak commitment is passed to storage without first requiring 32 bytes (`handlers_cert.go:29–43`). A malformed key produces lookup/error behavior, not a cryptographic bypass. | Exclude: input validation and error clarity; no asset-loss path. |
| EDA-09 | 22 | Informational | Empty low-level revert data maps to `INTERNAL_ERROR` (`EigenDACertVerifier.sol:97–136`). It never maps to `SUCCESS`; malformed/failed verification remains fail closed. | Exclude: error classification only. |
| EDA-10 | 23 | Informational | `verifySecurityParams` indexes batch arrays using the blob-parameter length without checking equal lengths (`verifier.go:188–228`), so mismatches can panic. | Exclude: verifier availability only; no invalid certificate is accepted. |
| EDA-11 | 24 | Informational | Protobuf quorum numbers are truncated from `uint32` to `uint8` (`certificate.go:109–129`). The verifier recomputes Merkle inclusion and compares security parameters after conversion (`verifier.go:98–120`); the report states only potential incorrect processing and gives no certificate that bypasses those bindings. | Exclude: representation validation/hardening without a demonstrated invalid-certificate acceptance or asset-loss sequence. |
| EDA-12 | 25 | Informational | `parseReturnEncodedPayloadQueryParam` prints an untrusted boolean-like query value (`routing.go:162–175`). | Exclude: production logging hygiene; the value is not a secret or asset authorization. |
| EDA-13 | 26 | Informational | Admin routes exist only when `AdminAPIType` is explicitly enabled, and the source says the proxy is not meant to be public (`routing.go:120–130`). The PUT handler parses only predefined EigenDA backend enums and toggles dispersal backend (`handlers_misc.go:53–105`). | Exclude: optional configuration authentication/hardening. No arbitrary transfer destination, authorization bypass over assets, or concrete loss is shown. |
| EDA-14 | 27 | Informational | `MaxQuorumID` is 254 (`core/v2/types.go:435–440`) while the pinned middleware contract supports 192 quorums. Unsupported values fail against on-chain constraints rather than bypass them. Both cited roots are outside the report's strict scope, and dependencies are excluded. | Exclude: inconsistent limit and out-of-scope report item; no security-check bypass or asset loss. |
| EDA-15 | 28 | Informational | A failed Ethereum `eth_call` returns an internal error (`cert_verifier.go:94–104`) and the report recommends external RPC failover. | Exclude: short-lived verification availability/retry behavior only. |
| EDA-16 | 29–31 | Informational | Five general comments cover an implicit zero return on short chains, an inaccurate version comment, an inaccurate error message, spelling, and comment formatting. The report expressly says these have no direct security implications. | Exclude: diagnostics, documentation, and style only. |

Selected distinct loss-of-assets root causes: **0**.

Creating a zero-finding task or strengthening any report item into an
unsupported asset-loss claim would violate the detect-only candidate contract.
