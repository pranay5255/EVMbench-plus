# Repository grounding — VII Finance

The PDF's repository and commit hyperlinks resolve to public repository
`kankodu/vii-finance-smart-contracts` at exact vulnerable commit
`2a3a72c675a580dcdeb2f7d733d40c6bfb1b3dc7`. The object is a commit with root
tree `93e281561e07ae50cbbf4d08eef6c2d7a5fb6f48` and was checked out detached in
an isolated clone.

All seven PDF-scoped Solidity paths exist at that commit. The vulnerable
operations and the report's cited remediation commits align:

- H-1: `UniswapV4Wrapper._unwrap` transfers fee shares without decrementing
  `tokensOwed`; fix `8c6b6cc…` subtracts the paid amounts.
- H-2: `ERC721WrapperBase.normalizedToFull` multiplies by global total supply;
  fix `b7549f2…` uses the sender's token balance.
- M-1: the base full unwrap lacks V4 fee settlement; fix `bf5f099…` adds and
  invokes `_settleFullUnwrap`.
- M-2: three-argument `Math.mulDiv` rounds down; fix `5e825d5…` requests
  `Math.Rounding.Ceil`.

The exact required import graph compiled offline. The repository's nested
Euler oracle declares an optional Redstone submodule whose historical object is
no longer exposed by the upstream. It is not imported by any compiled VII
source, was not replaced with a nearby commit, and is explicitly excluded from
the image's required dependency set. The public repository reports
`NOASSERTION` for its SPDX license, which remains a reviewer judgment before
publication.
