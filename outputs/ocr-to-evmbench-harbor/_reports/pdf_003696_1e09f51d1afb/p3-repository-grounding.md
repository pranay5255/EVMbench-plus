# EigenDA exact repository grounding

## Identity and scope

The report's short vulnerable commit resolves unambiguously in the public
`Layr-Labs/eigenda` repository. The isolated checkout is detached at
`066f8ef4f93bb8ce196555904e89adf7ef50e57f`; its root tree is
`c3d52e52d6471ead466775bc80b40b35c62a4f08`, with parent
`d5eec17de570d20d4e24ad53146ad8df4dce54cb`. GitHub's commit API returns the
same commit, tree, parent, date, and repository. The report's fixed short SHA
also resolves, separately, to
`794c356269b2e9559b6d43e4b21dee7c45eb354b`; it was not used as the task base.

All report-included path roots exist at the vulnerable commit. Their Git tree
objects are:

| Scope root | Git tree |
|---|---|
| `api/clients` | `ac91c58f6eb7db5f522b5d93a4d230530343ebc3` |
| `api/proxy` | `c145d5e6e2ad97cc4f6fef5e5501c00dfad0346b` |
| `contracts/src/integrations/cert` | `3a33808e0388f589f9cc34f12520b5095080f370` |
| excluded `contracts/src/integrations/cert/legacy` | `3f0ac037837057d4b409346d52b6d59464f3d06d` |

The checkout contains 230 tracked files under the two Go roots and 15 under
the certificate root, five of which are in excluded `legacy`. Its 22 pinned
recursive submodule-status lines hash to
`58f6a64ea7fca48f61c1d6915609b976eeb866e381fb48a1e0831ed299d70922`.
The tracked worktree was clean after removing a dependency lockfile generated
only by the disposable baseline installation.

## Framework and baseline

`go.mod` declares module `github.com/Layr-Labs/eigenda`, Go 1.24, and
toolchain Go 1.24.4. `contracts/foundry.toml` pins solc 0.8.12;
`contracts/package.json` builds with dependency installation followed by
`forge build`. The mixed Go/Foundry baseline is recorded separately in
`p5-build-baseline.md`.

## Code anchors and content hashes

All line anchors below refer to the exact vulnerable commit. The hashes bind
the reviewed file contents independently of mutable branch names.

| File | Relevant lines | SHA-256 |
|---|---:|---|
| `api/proxy/server/handlers_misc.go` | 45–123 | `fe8b233619afe0d7f100b4d237781bcd7b97534e0753b8bc4c038f88c4f7fd08` |
| `api/proxy/server/handlers_cert.go` | 29–54 | `fe11aec722c60e2b606e6179b96ec4a30537e3c31251fa45e137854cc72dfbe4` |
| `api/proxy/server/routing.go` | 35–70, 113–175 | `26c102a0105b8c79b6df1d57766361d9ad3b80209ce7269f7da05745b468de22` |
| `api/proxy/store/generated_key/eigenda/verify/verifier.go` | 91–123, 188–238 | `f98b90581e299faf58ce8a1ba3988ab17cbc79533334c19c8627c7d858532fc3` |
| `api/proxy/store/generated_key/eigenda/verify/certificate.go` | 59–129 | `fb5b6952d72d5e8b934f71cf46010ba658d95b5168ae527fb41051da4a48d1ed` |
| `api/clients/retrieval_client.go` | 181–217 | `04ecd30de72996dc495cf30065686a1c7afbd775f1785368fc70aac16ffc8872` |
| `api/clients/node_client.go` | 79–157 | `30a04a00b1fb5cc2e34be38832937a3a7e5cc5d20ebff856acc7e37367a7fdbc` |
| `api/clients/v2/accountant.go` | 177–220 | `073ca403d0e0efe63d34430bdf4aab5031708a68bee0617a28c6a2fc1822ca56` |
| `api/clients/v2/validator/internal/validator_grpc_manager.go` | 65–95 | `75584cda42cb69278a82deac8dcf673cb3851b709aa1aaf86be7925dfea3ab7c` |
| `api/clients/v2/verification/cert_verifier.go` | 85–105 | `3390c84b526a3eb15b84cf2881a709ac3c72bfcba683dc898b92416ffab77971` |
| `contracts/src/integrations/cert/EigenDACertVerifier.sol` | 88–145 | `f0f1b3d1e3d42a1b16f08a745ad6afa6eaff97a43672eafe4bf4652b95bc64d1` |
| out-of-scope `contracts/src/core/PaymentVault.sol` | 75–104 | `294ac90a0dbb94fc771891d17173084a9feaf1f569f43ab4fbb336b47a910f5a` |
| out-of-scope `core/v2/types.go` | 435–440 | `37cebbe920e97574ebb780968f1ecfc40c1a1a3e6b9fc7cb7101341e7c8827` |

## Scope inconsistencies and leakage boundary

The PDF's strict path statement conflicts with two finding asset lists:
EDA-06 partly cites `contracts/src/core/PaymentVault.sol`, and EDA-14 cites
`core/v2/types.go` plus `contracts/src/core/EigenDARegistryCoordinatorStorage.sol`.
Both are outside the strict allowlist; the lower on-chain limit comes from an
excluded pinned middleware dependency. The review keeps
the strict PDF scope and treats those paths only as corroboration; it does not
broaden the candidate scope.

The exact source tree also tracks five PDFs, including an audit report under
`api/proxy/docs/audits/`. Its SHA-256 differs from the host source PDF, but any
future candidate packaging would still have to exclude audit documents to
satisfy the leakage boundary. No candidate or image was created in this run.
