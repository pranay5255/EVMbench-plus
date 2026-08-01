# P3 repository grounding — Lido v3

Status: **PASS**

## Resolved snapshot

- Repository: `https://github.com/lidofinance/core.git`
- Vulnerable commit:
  `22cab0f0372015f2d2fce8bede64e98beae28571`
- Root tree:
  `0204ee9df364357c27e683434ef3129c7b70a81e`
- Checkout: detached, clean, isolated under `/tmp`
- Recursive submodule:
  `foundry/lib/forge-std@8f24d6b04c92975e0795b5868aa0d783251cdeaa`
- Tracked PDF/JSONL files: `0`

The initial commit matches both page-5 GitHub annotations and page 6 of the
report. Later re-audit and final commits remain separate from the vulnerable
task snapshot.

## Exact task identity

```text
lidofinance/core@22cab0f0372015f2d2fce8bede64e98beae28571|contracts/0.4.24/Lido.sol+contracts/0.8.9/Accounting.sol|detect
```

SHA-256:
`a402c4c8d352ae352afc528a3de050675490358dd6cad4d9b4722505dc32a802`

The two audited entry points are kept exact. Cross-contract tracing into
VaultHub, AccountingOracle, WithdrawalQueue, and OracleReportSanityChecker is
dependency evidence and does not silently broaden the report-declared scope.

## Audited file evidence

| Path | Git blob | SHA-256 |
|---|---|---|
| `contracts/0.4.24/Lido.sol` | `5732480f06c400933b89c0eccc52fd0a449c6af8` | `1be0fd7523df23e916bcc3130bb517c0a8c9fd77afcfa12cd543ad7575ce5f21` |
| `contracts/0.8.9/Accounting.sol` | `cabed2c31475ee490934e31fc36340f50b787398` | `8f5b456caeec50f63f75150229c9315f970c99db0900bc4738485c08773330ff` |
| `contracts/0.8.25/vaults/VaultHub.sol` | `54275b03cf507cc2ff3df09fe7695104963b0383` | `adf8eed681a14184caecf7871a94325b5ff5432f1d7081fde0071ee27232161b` |
| `contracts/0.8.9/sanity_checks/OracleReportSanityChecker.sol` | `d6cb0c6dca00e624a27b7585d6e913754949515a` | `a9af376b8f34b312f464e85a8797054e14396d62743e4084ab3a5651a083d4a7` |
| `contracts/0.8.9/WithdrawalQueue.sol` | `733c4a830c4515743969d32d77fa32505e44e9e6` | `efa5a32fbc99cafdb16a38d96a9bb5b29a62e60b5610e7c317711cc58402b131` |
| `contracts/0.8.9/oracle/AccountingOracle.sol` | `0d3e9b1788d5be51b998f3fa223ed1bde9ec88a3` | `b3557bb25649701c42a39a035b8d826b857a8c725ca0f50cba141664da14b748` |
