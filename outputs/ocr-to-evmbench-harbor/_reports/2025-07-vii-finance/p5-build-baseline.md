# Source build baseline — VII Finance

The exact detached checkout at
`2a3a72c675a580dcdeb2f7d733d40c6bfb1b3dc7` compiled all 183 reachable Solidity
files with Solidity `0.8.26+commit.8a97fa7a` inside local image
`evmbench/base:latest` using Foundry `1.3.6`.

The compiler binary SHA-256 is
`d5f23436f443edb85d8e76906d12f0a86ce0490e7663a9e608efeb7a93f149ef`,
matching the official Solidity manifest. After that binary and the exact
required submodules were cached, `forge clean && forge build` passed with
container networking disabled.

Network-disabled tests also passed:

- `test/ERC721WrapperBase.t.sol`: 9/9;
- `test/uniswap/factory/UniswapV3WrapperFactory.t.sol`: 1/1;
- `test/uniswap/factory/UniswapV4WrapperFactory.t.sol`: 1/1.

The remaining Uniswap integration suites require `MAINNET_RPC_URL` and a fork
at block 22,473,612, so they were not treated as offline baseline tests. No
report PoC patch was applied to the vulnerable source.
