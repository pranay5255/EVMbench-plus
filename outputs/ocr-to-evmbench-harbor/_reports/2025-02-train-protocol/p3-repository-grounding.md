# P3 repository grounding — Train Protocol

Status: **PASS**

## Resolved vulnerable snapshot

- Repository:
  `https://github.com/layerswap/layerswap-atomic-bridge.git`
- Vulnerable commit:
  `6c96f61d7d6c7e8a8991a12e40068ab53b0a9e7b`
- Root tree:
  `c15b19365d49f1e4e6a09d45c6f1dc07cb34d1ae`
- Commit subject:
  `refactor redeem function in EVM(native/ERC20)`
- Checkout: detached, clean, isolated under `/tmp`
- Recursive submodules: none
- Tracked PDF/JSONL files: `0`

The full commit is present in the report's page-5 annotations and can be
checked out directly from the named public repository.

## Exact task identity

```text
layerswap/layerswap-atomic-bridge@6c96f61d7d6c7e8a8991a12e40068ab53b0a9e7b|chains/evm/solidity/contracts/HashedTimeLockERC20.sol+chains/evm/solidity/contracts/HashedTimeLockEther.sol+chains/starknet/src/HashTimeLockedERC20.cairo|detect
```

SHA-256:
`7ee200d42e8b9d1ea9613abb01b9ae9f8ad5e5e38bd0a7ba8446af128f2b1b29`

## Audited file evidence

| Path | Git blob | SHA-256 |
|---|---|---|
| `chains/evm/solidity/contracts/HashedTimeLockERC20.sol` | `8b0ddbfc0c3e375bb4f8f8b403f05509a80e463b` | `65814897b9b033b6f4e1c08c8b451f558ae62bda881925efae019d3906f3f995` |
| `chains/evm/solidity/contracts/HashedTimeLockEther.sol` | `1fc361cf7b4522d3828d5294880297a95cbc2e26` | `24e1ba44bcfc452a9da5f9621d2c37db779d1668e9ac8b03a79f09e266eb4130` |
| `chains/starknet/src/HashTimeLockedERC20.cairo` | `b912140af3d0ff24a6a46c8849c339059c0def16` | `c78e97ee59ff082f9b58b8dde23373207619e8bb0610796cb62724ff2b162e0f` |

The report snippets, identifiers, and affected functions match these exact
files.

## Post-audit repository boundary

The two report-labeled later commits exist in
`TrainProtocol/contracts`, but the vulnerable commit does not. They are kept
as separate host-side corroboration and are not reachable in the agent image.
The benchmark snapshot remains the exact repository and commit named by the
report.
