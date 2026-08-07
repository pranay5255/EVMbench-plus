# Vulnerable-snapshot build and unit baseline

The detached, recursively initialized checkout at `60c462d6...` was built with
Foundry `1.7.1` (commit `4072e48705af9d93e3c0f6e29e93b5e9a40caed8`)
and official Solidity
`0.8.25+commit.b61c2a91.Linux.g++`. The downloaded solc binary matched the
official SHA-256
`c42aada7a52057ddbed93ec011235e256c564c440b68dbaac5ae482babbb3d6d`.

`forge build --use /tmp/mellow-review.xSrGG4/solc-0.8.25` completed
successfully and compiled 203 files. The focused OracleHelper unit suite passed
19/19 with the report's fork block number (`22730425`) and a stable local
timestamp (`1750000000`). The full `test/unit/**` suite then exited zero under
the same block/timestamp; `forge test --list --json` enumerated 45 contracts and
454 test entries.

An initial test invocation at Foundry's default timestamp `1` failed because
`Oracle.submitReports` subtracts configured report intervals from
`block.timestamp`. This is a test-environment timestamp underflow, not a source
build failure. The stable timestamp rerun passed. Two Foundry fuzz failure-cache
files emitted into the parent working directory by that initial invocation were
identified by timestamp and removed; the parent returned to its sole
pre-existing ledger modification.

The report's integration suite was not replayed because its configuration
requires `ETH_RPC`. No live RPC credential was used or copied. The report itself
records a final-commit fork run at block `22730425` with 430 passing tests;
that evidence does not substitute for execution at the vulnerable snapshot.

No model/agent smoke was authorized or run. No canonical image was built at
this pre-approval checkpoint.
