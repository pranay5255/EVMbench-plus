# P4 finding grounding: H-01 (C-1)

## Report claim

Section 7.1.1 (pages 10–11) states that
`SecuritizeOnRamp::executePreApprovedTransaction` verifies an EIP-712 signature
that includes a nonce but never checks that the provided nonce equals
`noncePerInvestor[txData.senderInvestor]`. The function only increments the
stored nonce after signature recovery, enabling replay of old signatures.

## Code verification at a944bb11b106c13a5e43f8de01c9c01eeb5bb472

File: `contracts/on-ramp/SecuritizeOnRamp.sol`

- `noncePerInvestor` mapping at line 44
- `nonceByInvestor` view at lines 114–116
- `executePreApprovedTransaction` at lines 185–199:
  - `hashTx(txData)` then `ECDSA.recover`
  - role check against TRUST_SERVICE EXCHANGE/ISSUER
  - unconditional `noncePerInvestor[...] += 1`
  - `Address.functionCall(txData.destination, txData.data)`
  - **no** comparison of `txData.nonce` to storage
- `hashTx` private helper encodes `txData.nonce` into the EIP-712 struct hash

Git blob: `b4bdc26808e5679df672c9957607be086c2e9102`
SHA-256: `3e10a580b9ad5a7b3dfcc98898e20ab24e7e726e3b31663f0d8cd3d37500c2ed`

## Asset-loss path

The report PoC shows a subscribe/swap path executed twice with one signature:
investor DS-token balance doubles and USDC is fully spent. That is direct
double-spend of investor liquidity and unauthorized second issuance/transfer of
DS tokens under the `loss_of_assets` policy.

## Fix corroboration (not the task snapshot)

Commit `65179bcf41ed859106069dcaa751f5a2cec3038e` changes `hashTx` to hash
`noncePerInvestor[txData.senderInvestor]` instead of `txData.nonce`, invalidating
replays. Present only as remediation evidence.

## OCR corrections

OCR misspellings such as `SecuritieOnRamp`, `IDStrustService`, and truncated
function bodies were corrected from the hash-verified PDF and the detached
checkout. OCR slices remain byte-identical to the immutable JSONL rows.
