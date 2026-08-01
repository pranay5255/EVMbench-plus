# P5 build and test baseline: `2025-01-burve`

Status: build passed; upstream tests disclosed with failures.

The audited checkout requires Solidity 0.8.27. The official Linux binary
`solc-linux-amd64-v0.8.27+commit.40a35a09` was verified at SHA-256
`b9977d500c17cba6f0032ca939ef98c4decf6363f19f386d05fb02f708115264`.

The reproducible build command uses Foundry 1.7.1, offline compiler resolution,
IR compilation, optimization, and the more-specific OpenZeppelin remapping:

```text
forge build --force --offline --use /tmp/solc-0.8.27 --via-ir --optimize \
  --remappings @openzeppelin/=lib/openzeppelin-contracts/contracts/ \
  --remappings @openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/
```

The no-cache image build and a fresh `--force` rebuild in a container with
`--network none` both pass. Compiler warnings are upstream warnings and include
the malformed shift diagnostics in the vulnerable source.

The unmodified upstream suite is not green: 11 tests pass and 16 fail across 27
tests. Failures include setup `EvmError: Revert`, three cheatcode call-depth
expectation mismatches, and one log mismatch. This is recorded as the
vulnerable baseline; it is not presented as candidate semantic validation and
no finding-specific tests were added.
