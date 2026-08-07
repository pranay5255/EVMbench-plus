# [H-01] Incorrect HTTP header key breaks JSON response metadata

## Source report

- Report finding: EDA-01, Medium
- PDF pages: 8–9
- Broader-task class: response correctness and client interoperability

## Affected code

- `api/proxy/server/handlers_misc.go`: `writeJSON`

## Root cause

`writeJSON` passes the MIME value `application/json` as the header map key
instead of using the `Content-Type` header name. Go therefore emits a header
whose name is effectively `Application/Json`, while the real content type is
left unset and may be inferred as a generic text type.

## Prerequisites

- A client calls an endpoint that returns data through `writeJSON`.
- The client or an intermediary relies on the response `Content-Type` to
  select its parser, cache policy, or response validation.

## Failure sequence

1. The handler successfully serializes its response as JSON.
2. `writeJSON` calls `w.Header().Set(contentTypeJSON, "application/json")`.
3. The response lacks the intended `Content-Type: application/json` metadata.
4. A strict client, proxy, or cache treats the response as the wrong media
   type even though its body is valid JSON.

## Impact

Valid API responses can be rejected, misparsed, or cached under inappropriate
rules. The defect breaks interoperability for every handler using this helper.
It is included under the user-authorized broader bug policy; it does not claim
asset loss.

## Code evidence

At vulnerable commit `066f8ef4f93bb8ce196555904e89adf7ef50e57f`,
`handlers_misc.go:108–119` serializes the object and then sets:

```go
w.Header().Set(contentTypeJSON, "application/json")
w.WriteHeader(http.StatusOK)
_, err = w.Write(jsonData)
```

The file already uses the correct header key constant elsewhere:

```go
w.Header().Set(headerContentType, contentTypeJSON)
```

## Remediation

Set `headerContentType` to `contentTypeJSON` before writing the status and add
an HTTP test that asserts both the exact header and body.
# [H-02] Blob retrieval ignores context cancellation and can outlive callers

## Source report

- Report finding: EDA-02, Low
- PDF pages: 10–11
- Broader-task class: cancellation, resource lifetime, and availability

## Affected code

- `api/clients/retrieval_client.go`: `RetrieveBlobChunks`

## Root cause

The retrieval client submits one worker for each operator and then performs one
unconditional receive from `chunksChan` per operator. The collection loop does
not select on `ctx.Done()` and the worker pool is not stopped as soon as the
caller cancels or enough valid chunks have been collected.

## Prerequisites

- A retrieval involves one or more slow or unresponsive operators.
- The caller cancels or reaches its deadline before all worker results arrive.

## Failure sequence

1. `RetrieveBlobChunks` schedules a request for every operator.
2. The caller's context is cancelled while one or more requests remain.
3. The collection loop remains blocked on `reply := <-chunksChan` rather than
   returning immediately on `ctx.Done()`.
4. The request and its worker resources stay live until all expected sends or
   lower-level timeouts complete.

## Impact

Cancelled work consumes goroutines, connections, and request capacity and
increases tail latency. Repeated cancelled retrievals can degrade service
availability. This is a broader availability finding, not an asset-loss claim.

## Code evidence

`retrieval_client.go:181–217` creates the channel and workers, then waits with:

```go
for i := 0; i < len(operators); i++ {
    reply := <-chunksChan
    // validate or skip the reply
}
```

The nearby TODO acknowledges that remaining RPC calls are not cancelled after
enough chunks are gathered.

## Remediation

Use a derived cancellable context, select between `chunksChan` and
`ctx.Done()`, stop remaining work when reconstruction requirements are met,
and ensure the worker pool is released on every return path.
# [H-03] Retrieval connections are never closed and exhaust resources

## Source report

- Report finding: EDA-03, Low
- PDF pages: 12–13
- Broader-task class: connection leak and availability

## Affected code

- `api/clients/node_client.go`: `GetChunks`
- `api/clients/retrieval_client.go`: concurrent caller of `GetChunks`

## Root cause

Every `GetChunks` invocation constructs a new gRPC `ClientConn`, but no return
path closes it. A blob retrieval invokes this method concurrently for many
operators, so both successful and failed RPC cycles accumulate transports and
file descriptors.

## Prerequisites

- The retrieval client processes repeated blob requests.
- Each request contacts multiple operators through `GetChunks`.

## Failure sequence

1. `grpc.NewClient` creates a connection for an operator.
2. `GetChunks` performs `RetrieveChunks` and returns a result through the
   channel.
3. The function returns without calling `conn.Close()`.
4. Repeated retrievals accumulate live connections and descriptors until
   process or host limits are reached.

## Impact

The client can lose the ability to open new sockets or files, causing broad
retrieval failures and requiring a restart. This is an availability and
resource-management defect under the broader task policy.

## Code evidence

`node_client.go:88–111` assigns `conn` and immediately constructs the RPC
client. The only deferred cleanup is for the per-call context:

```go
conn, err := grpc.NewClient(...)
// ...
nodeCtx, cancel := context.WithTimeout(ctx, c.timeout)
defer cancel()
```

There is no `defer conn.Close()` after the successful constructor check.

## Remediation

Close the connection on every return path or, preferably, reuse a bounded
connection pool keyed by operator endpoint. Add a stress test that verifies
descriptor counts remain stable across repeated retrievals.
# [H-04] Failed gRPC client construction triggers a nil cleanup panic

## Source report

- Report finding: EDA-04, Low
- PDF pages: 14–15
- Broader-task class: panic and availability

## Affected code

- `api/clients/v2/validator/internal/validator_grpc_manager.go`: operator
  chunk retrieval

## Root cause

The function registers a deferred `conn.Close()` immediately after
`grpc.NewClient`, before checking its returned error. If construction fails and
does not yield a usable connection, function return executes the defer and
dereferences an invalid `conn`.

## Prerequisites

- An operator socket is malformed or otherwise causes `grpc.NewClient` to
  return an error.
- The error path returns from the function.

## Failure sequence

1. `grpc.NewClient` returns an error and no usable connection.
2. A closure that calls `conn.Close()` has already been deferred.
3. The function detects `err` and returns its formatted error.
4. Deferred cleanup runs during unwinding and panics instead of preserving the
   original error.

## Impact

A malformed or failed endpoint can crash the validator client process rather
than producing a controlled per-operator failure. This is a broader
availability finding and does not assert asset loss.

## Code evidence

`validator_grpc_manager.go:73–86` has this order:

```go
conn, err := grpc.NewClient(...)
defer func() {
    err := conn.Close()
    // ...
}()
if err != nil {
    return nil, fmt.Errorf("failed to create connection ...")
}
```

## Remediation

Check `err` before registering cleanup. After confirming `conn` is usable,
defer its close and keep any cleanup error separate from the constructor
error.
# [H-05] Unbounded commitment paths enable memory-exhaustion denial of service

## Source report

- Report finding: EDA-05, Low
- PDF page: 16
- Broader-task class: remotely triggered resource exhaustion

## Affected code

- `api/proxy/server/routing.go`: Optimism generic commitment GET route

## Root cause

The route constrains the prefix, commitment type, DA-layer byte, and version
byte but captures the remaining hexadecimal payload without an upper bound.
The HTTP stack and router therefore accept and materialize an arbitrarily long
path variable before later processing can reject it.

## Prerequisites

- The proxy HTTP endpoint is reachable.
- A requester can send very long generic-commitment paths.

## Failure sequence

1. A requester supplies a syntactically matching path with an extremely long
   payload suffix.
2. The server parses and stores the whole URL and captured route variable.
3. Downstream decoding or logging creates additional allocations proportional
   to attacker-controlled input size.
4. Concurrent requests consume heap and CPU until the proxy slows, is killed,
   or becomes unavailable.

## Impact

An unauthenticated requester can cause excessive memory consumption and
service interruption. The report classifies this as denial of service; the
broader candidate includes it without claiming an asset-loss consequence.

## Code evidence

`routing.go:45–59` ends the route with an unconstrained variable:

```go
"{" + routingVarNamePayloadHex + "}"
```

The preceding bytes have regular-expression limits, but the payload component
has neither a fixed length nor a maximum.

## Remediation

Constrain the payload to the exact supported encoded lengths and reject
oversized request targets at the HTTP-server boundary before routing or
decoding.
# [H-06] A zero reservation window panics payment accounting

## Source report

- Report finding: EDA-06, Low
- PDF pages: 17–18
- Broader-task class: unsafe configuration handling and client availability

## Affected code

- `api/clients/v2/accountant.go`: `SetPaymentState` and
  `getOrRefreshRelativePeriodRecord`

The report also cites `contracts/src/core/PaymentVault.sol`, which is outside
its own strict path allowlist. This candidate scores only the in-scope Go
client defect.

## Root cause

`SetPaymentState` accepts a global `reservationWindow` of zero without
validation. Later accounting divides the requested period index by that value
before selecting a circular-buffer record, causing Go's integer
divide-by-zero panic.

## Prerequisites

- The disperser's payment-state response contains a zero reservation window.
- The accountant processes usage that calls
  `getOrRefreshRelativePeriodRecord`.

## Failure sequence

1. `SetPaymentState` copies the zero global value into
   `a.reservationWindow`.
2. Accounting derives a period index using the stored window.
3. `index / reservationWindow` executes with a zero divisor.
4. The Go process panics instead of rejecting the invalid payment state.

## Impact

A bad global payment parameter can crash clients and prevent blob dispersal or
payment processing until the state is corrected and clients restart. The
finding is included as a broader crash/availability defect, not as a
misbilling or asset-loss claim.

## Code evidence

`accountant.go:189–201` calculates:

```go
relativeIndex := uint32((index / reservationWindow) % uint64(len(a.periodRecords)))
```

`accountant.go:210–220` validates that the response objects are non-nil but
copies `GetReservationWindow()` without checking that it is nonzero.

## Remediation

Reject a zero reservation window in `SetPaymentState` before mutating
accountant state and retain the last known-valid state on an invalid response.
# [H-07] Unknown chunk encodings leave invalid nil frames

## Source report

- Report finding: EDA-07, Low
- PDF page: 19
- Broader-task class: unsafe enum handling and retrieval availability

## Affected code

- `api/clients/node_client.go`: `GetChunks`

## Root cause

The switch that deserializes returned chunks has explicit cases for `GNARK`,
`GOB`, and `UNKNOWN`, but no `default`. Protobuf permits unknown numeric enum
values on the wire. Such a value executes no branch, leaves `chunk` nil and
`err` unchanged, and stores the nil frame as if deserialization succeeded.

## Prerequisites

- A node returns a chunk-encoding enum value unknown to this client version.
- The response contains one or more chunk byte strings.

## Failure sequence

1. The RPC succeeds with an unrecognized enum number.
2. No switch case runs for a returned chunk.
3. The nil `chunk` is inserted into the result slice because `err` remains
   nil.
4. Verification receives invalid frame data and errors or panics deeper in the
   retrieval path.

## Impact

Version skew or a malformed peer response can turn a controlled protocol error
into nil-data propagation and retrieval failure. This is a broader correctness
and availability defect.

## Code evidence

`node_client.go:121–150` initializes `var chunk *encoding.Frame`, handles
three named cases, omits `default`, and then unconditionally executes:

```go
chunks[i] = chunk
```

## Remediation

Add a default branch that returns an explicit unsupported-format error before
writing the chunk. Test with a protobuf enum number not known to the generated
client.
# [H-08] Wrong-length keccak commitments reach the storage lookup

## Source report

- Report finding: EDA-08, Low
- PDF pages: 20–21
- Broader-task class: input validation and error handling

## Affected code

- `api/proxy/server/handlers_cert.go`: `handleGetOPKeccakCommitment`

## Root cause

The handler hex-decodes the commitment captured from the route but does not
require the 32-byte length of a Keccak-256 commitment. Any even-length hex
string can therefore pass parsing and be used as an S3 lookup key.

## Prerequisites

- A requester supplies a route value that is valid hexadecimal but not 32
  bytes long.

## Failure sequence

1. The router captures the malformed commitment string.
2. `hex.DecodeString` succeeds because the characters and parity are valid.
3. The handler calls `GetOPKeccakValueFromS3` with a semantically invalid key.
4. Storage lookup and generic error handling run instead of returning an
   immediate structured parsing error.

## Impact

Malformed identifiers reach the storage layer, produce misleading not-found or
backend errors, add avoidable load, and weaken the API's type contract. This
broader task scores the missing validation, not a cryptographic bypass.

## Code evidence

`handlers_cert.go:29–43` verifies presence and hex syntax, then directly calls:

```go
payload, err := svr.keccakMgr.GetOPKeccakValueFromS3(r.Context(), keccakCommitment)
```

No `len(keccakCommitment) == 32` invariant appears between decoding and lookup.

## Remediation

Reject any decoded value whose length is not exactly 32 bytes and return the
same structured parsing error class used for malformed hexadecimal input.
# [H-09] Mismatched security-parameter arrays panic the verifier

## Source report

- Report finding: EDA-10, Informational
- PDF page: 23
- Broader-task class: malformed-certificate handling and verifier availability

## Affected code

- `api/proxy/store/generated_key/eigenda/verify/verifier.go`:
  `verifySecurityParams`

## Root cause

The loop uses the number of blob quorum parameters as its bound while indexing
two independent batch-header arrays at the same position. It never checks that
`GetQuorumNumbers()` and `GetQuorumSignedPercentages()` are at least as long
as `blobHeader.QuorumBlobParams`.

## Prerequisites

- Certificate data reaches verification with more blob quorum parameters than
  corresponding batch-header quorum or signed-percentage entries.

## Failure sequence

1. `verifySecurityParams` starts iterating over the longer blob parameter
   slice.
2. At the first missing batch entry, an expression indexes past the end of a
   batch slice.
3. Go raises an array-bounds panic rather than returning a validation error.
4. The verifier request—and potentially its hosting process—fails.

## Impact

Malformed or inconsistent certificate structures can crash verification and
turn bad input into service disruption. No invalid certificate is accepted;
the broader candidate scores failure isolation and availability.

## Code evidence

`verifier.go:188–228` begins:

```go
for i := 0; i < len(blobHeader.QuorumBlobParams); i++ {
    if batchHeader.GetQuorumNumbers()[i] !=
        blobHeader.QuorumBlobParams[i].QuorumNumber {
        // ...
    }
    // later: batchHeader.GetQuorumSignedPercentages()[i]
}
```

## Remediation

Validate equality of all correlated array lengths before the loop and return a
typed malformed-certificate error on any mismatch.
# [H-10] Unchecked quorum downcasts silently truncate certificate data

## Source report

- Report finding: EDA-11, Informational
- PDF page: 24
- Broader-task class: malformed-certificate validation and data integrity

## Affected code

- `api/proxy/store/generated_key/eigenda/verify/certificate.go`:
  `ReadBlobHeader`

## Root cause

The protobuf representation exposes quorum numbers and threshold percentages
as `uint32`, but `ReadBlobHeader` casts them directly to `uint8` without
checking their ranges. Values above 255 wrap modulo 256, so the verifier no
longer evaluates the values that appeared on the wire.

## Prerequisites

- A malformed or future-version certificate contains a quorum number or
  threshold greater than 255.

## Failure sequence

1. Protobuf parsing preserves an out-of-range `uint32` value.
2. `ReadBlobHeader` converts it directly with `uint8(...)`.
3. High bits are discarded silently.
4. Merkle and security-parameter processing operate on the truncated value or
   produce confusing mismatches instead of rejecting the certificate at the
   representation boundary.

## Impact

Certificate validation is non-canonical for out-of-range inputs and may process
a different quorum identifier or threshold from the serialized message. The
report does not establish a successful security bypass; this broader task
scores the concrete truncation bug.

## Code evidence

`certificate.go:109–129` constructs each `QuorumBlobParam` with:

```go
QuorumNumber:                    uint8(qp.GetQuorumNumber()),
AdversaryThresholdPercentage:    uint8(qp.GetAdversaryThresholdPercentage()),
ConfirmationThresholdPercentage: uint8(qp.GetConfirmationThresholdPercentage()),
```

Each cast is annotated to suppress the integer-conversion warning rather than
preceded by a bound check.

## Remediation

Validate the protocol maximum for every field before conversion. In
particular, reject quorum numbers above the on-chain maximum and percentages
outside their valid range.
# [H-11] Enabled backend administration endpoints lack authentication

## Source report

- Report finding: EDA-13, Informational
- PDF page: 26
- Broader-task class: administrative access control and configuration integrity

## Affected code

- `api/proxy/server/routing.go`: admin route registration
- `api/proxy/server/handlers_misc.go`:
  `handleSetEigenDADispersalBackend`

## Root cause

When `AdminAPIType` is enabled, the router publishes GET and PUT endpoints for
the active dispersal backend without any authentication or authorization
middleware. The implementation relies only on the deployment assumption that
the proxy will not be exposed publicly.

## Prerequisites

- The administrator enables the admin API.
- An unauthorized requester can reach the proxy listener through local,
  container, cluster, or public networking.

## Failure sequence

1. The server registers `/admin/eigenda-dispersal-backend` for GET and PUT.
2. A requester sends a PUT body selecting a recognized v1 or v2 backend.
3. The handler parses the enum and calls `SetDispersalBackend` without
   authenticating the caller.
4. Subsequent blob dispersals use the requester-selected backend.

## Impact

Any network-reachable caller can read and modify operational backend
configuration, causing unauthorized version changes, inconsistent behavior, or
service disruption. The handler does not grant arbitrary asset authority; it
is included under the broader administrative-security policy.

## Code evidence

`routing.go:120–130` conditionally registers both routes and explicitly notes
that no startup API key was implemented. `handlers_misc.go:53–105` reads the
body, converts a recognized backend string, and invokes:

```go
svr.SetDispersalBackend(backend)
```

No caller identity is checked in either path.

## Remediation

Require authenticated, authorized administration middleware and bind admin
routes to a separate restricted listener. Treat network placement as defense
in depth rather than the sole control.
# [H-12] Certificate validation has no Ethereum RPC failover

## Source report

- Report finding: EDA-15, Informational
- PDF page: 28
- Broader-task class: dependency resilience and verification availability

## Affected code

- `api/clients/v2/verification/cert_verifier.go`: `CheckDACert`

## Root cause

Certificate validation issues one `CallContract` through the configured
Ethereum client. Any transport, provider, or transient RPC failure is wrapped
as a generic `CertVerifierInternalError`; the error is not marked as
failover-eligible and no alternate provider is attempted.

## Prerequisites

- The configured Ethereum RPC endpoint is slow, unavailable, rate-limited, or
  returns a transient error while a certificate is checked.

## Failure sequence

1. `CheckDACert` packs the verifier contract call.
2. The sole configured RPC request fails.
3. The method returns `CertVerifierInternalError` immediately.
4. The proxy returns a server error; upstream software must wait and retry the
   entire certificate request even when another healthy RPC endpoint exists.

## Impact

A single-provider outage causes avoidable certificate-fetch failures and
short-lived rollup delays. The report describes retries and external failover
as operational mitigation; this broader candidate scores the missing
in-process classification/failover behavior.

## Code evidence

`cert_verifier.go:94–100` performs one call and returns directly on error:

```go
returnData, err := cv.ethClient.CallContract(ctx, ethereum.CallMsg{
    To:   &certVerifierAddr,
    Data: callMsgBytes,
}, nil)
if err != nil {
    return &CertVerifierInternalError{Msg: "checkDACert eth call", Err: err}
}
```

## Remediation

Classify transient RPC failures separately and retry through a bounded,
health-checked provider set. Preserve the original cause and do not retry
deterministic certificate-validation failures.
