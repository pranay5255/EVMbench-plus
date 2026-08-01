# EigenDA exact-source build and test baseline

The exact audited commit is buildable in both reviewed languages. This proves
snapshot/framework viability; it does **not** make a zero-finding source tree
an admissible EVMBench task.

## Solidity / Foundry

The disposable checkout's 22 recursive submodules were initialized. The
declared OpenZeppelin package dependencies were initially absent, so
`npm install --ignore-scripts --no-audit --no-fund` was run only under
`contracts/`; the generated untracked lockfile was removed afterward.

Using local image `evmbench/base:latest` (image ID
`sha256:fc20d776501708f9236e87b0e853d03f66d3b75af41a9ab1d1aad2c8b2c72fb9`,
repository digest
`pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0`),
Forge 1.3.6 compiled 216 source files successfully with solc 0.8.12. Focused
`PaymentVaultUnit` and `EigenDACertVerifierRouterUnit` suites passed 23 tests,
with zero failures and zero skips.

## Go

Using `golang:1.24.4-bookworm`, pinned to
`golang@sha256:10f549dc8489597aa7ed2b62008199bb96717f52a8e8434ea035d5b44368f8a6`,
all audited package groups compiled under `-mod=readonly`:

```text
go test -mod=readonly -run '^$' \
  ./api/clients/... \
  ./api/proxy/server \
  ./api/proxy/store/generated_key/eigenda/verify
```

Focused tests for payment-state validation, admin-backend routing, query
parsing, and commitment verification passed in all three selected package
groups.

A broader runtime attempt was intentionally not recorded as a full-suite pass:
some `api/clients` tests write SRS tables into the source tree, which was
mounted read-only, and `api/clients/v2` testcontainers require a nested Docker
daemon. The server/verifier subsets passed. These are test-environment
requirements, not compilation failures, and the limitation is retained rather
than masked.

No candidate source build, verifier image, Harbor replay, agent, or model smoke
was started because the semantic selection gate failed first.
