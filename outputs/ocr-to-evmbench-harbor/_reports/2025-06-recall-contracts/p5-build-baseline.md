# P5 build baseline: `2025-06-recall-contracts`

The host has no `forge` executable. The pinned EVMBench base image contains
Foundry `1.3.6-v1.3.6` but does not initially cache the repository's selected
Solc `0.8.30`; a read-only, network-disabled pre-build therefore reached
compiler selection and failed only while trying to fetch the Solidity compiler.

The first network-enabled no-cache candidate build then exposed an upstream
Foundry auto-remapping defect. Foundry inferred
`solidity-cborutils/=lib/filecoin-solidity/lib/solidity-cborutils/contracts/`,
so imports already containing `contracts/CBOR.sol` resolved to a duplicated
`contracts/contracts/CBOR.sol`. The candidate build supplies the explicit
environment-only remapping
`solidity-cborutils/=lib/filecoin-solidity/lib/solidity-cborutils/`; it does
not edit the audited checkout or any dependency file.

With that remapping, the exact checkout compiled all 182 source files. The
unmodified full upstream suite then ran 79 tests: 76 passed and 3 failed. Two
`LibWasm` tests fail because Foundry 1.3.6 reports a different nested
cheatcode/revert depth than the historical suite expects. The remaining
`ValidatorGater` failure is the legacy `testFailUnauthorizedApprove` naming
convention, which current Foundry rejects instead of interpreting as an
expected revert. No audited source, dependency, or test file was changed.

The candidate Docker build is permitted to use network during image
construction. It must install/cache the compiler, compile the exact shallow
snapshot, run all 20 unmodified `ValidatorRewarder` tests, and run the seven
current-Foundry-compatible unmodified `ValidatorGater` tests. This covers both
vulnerable `whenActive` paths, including existing tests that expressly expect
inactive calls to succeed without changing state. A subsequent fresh container
must repeat the same build and targeted tests with
`--network none` and `FOUNDRY_OFFLINE=true` before the review checkpoint can
pass. The 76/79 full-suite result remains a disclosed toolchain-compatibility
limitation; it is not represented as a fully green upstream baseline.

Foundry 1.3.6 also treats a populated Git submodule working tree as missing if
all nested `.git` markers are deleted, then invokes `git submodule update` even
with `--offline`. Retaining the original submodule object stores would make 31
excluded third-party OpenZeppelin audit PDFs recoverable from Git objects. The
image therefore removes all original nested Git metadata and those PDFs, then
creates an empty local `.git` marker in each of the 31 recursive dependency
directories. Each marker has no commit, object, or remote and excludes the
already-verified dependency working tree from local status discovery. This
minimal Foundry-compatibility shim permits a genuine network-disabled rebuild
without adding post-audit history or recoverable report evidence. The main
audited repository remains a clean, one-commit detached checkout. Acquisition,
verification, PDF removal, original submodule-metadata removal, and empty-marker
creation occur in one Docker construction layer so deleted report blobs and
historical objects cannot survive in a lower image layer.
