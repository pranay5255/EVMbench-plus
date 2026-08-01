# P5 build baseline — Train Protocol

Status: **PASS with upstream test-suite drift disclosed**

## Isolated source build

- Vulnerable HEAD:
  `6c96f61d7d6c7e8a8991a12e40068ab53b0a9e7b`
- Local Node: `20.19.6`
- Solidity compiler: `0.8.23`
- `npm ci`: failed on an upstream peer-dependency conflict between
  Hardhat Verify `1.1.1` and Ignition's `^2.0.1` requirement.
- `npm ci --legacy-peer-deps`: passed; `605` packages installed.
- `hardhat compile`: passed; `30` Solidity files compiled.
- Compiler warnings: unchecked low-level native-Ether call return values in
  `HashedTimeLockEther.sol`.

The compile required a non-secret dummy private-key-shaped value because the
upstream Hardhat config declares `[process.env.PRIV_KEY]` for every remote
network even when compiling locally.

## Upstream tests

`hardhat test` reaches no test body:

- `0` passed;
- `2` setup hooks failed.

The tests request artifacts named `HashedTimeLockERC20` and
`HashedTimeLockEther`, while the audited source files declare
`LayerswapV8ERC20` and `LayerswapV8`. This is upstream test-suite naming drift;
the candidate does not modify the vulnerable snapshot to hide it.

## Starknet

The Cairo file was verified byte-for-byte and reviewed against the report.
Scarb was not available in the review environment, so a Starknet build was not
run. This remains a reproducibility disclosure for human review.

## Agent image build

The candidate image independently:

- fetched only the exact vulnerable commit at depth 1;
- installed the locked EVM dependencies with legacy peer resolution;
- compiled all 30 Solidity files under Node `22.15.0`;
- preserved one reachable Git commit;
- ran no repository tests because the exact baseline's artifact-name mismatch
  is already established above.
