# P4 finding dispositions — Train Protocol

Status: **PASS**

Four of the report's nine findings have code-grounded direct or indirect
asset-loss paths in the exact vulnerable snapshot.

| Report ID | Pages | Severity | Status | Disposition | Candidate |
|---|---:|---|---|---|---|
| LYSWP2-7 | 10–11 | High | Fixed | Included: an LP can refund its earlier-expiring side and redeem the user's still-locked funds. | H-01 |
| LYSWP2-6 | 12–13 | Medium | Acknowledged | Included: nominal fee-on-transfer accounting consumes other deposits or leaves HTLCs insolvent. | H-02 |
| LYSWP2-8 | 14–16 | Medium | Fixed | Included: ignored Starknet transfer failures create unfunded cross-chain events or finalized unpaid claims. | H-03 |
| LYSWP2-5 | 17–18 | Low | Fixed | Included: the cached EIP-712 domain allows signatures to be replayed onto an unintended fork. | H-04 |
| LYSWP2-13 | 19–20 | Low | Fixed | Excluded: solver-side ID verification; documentation-only remediation and no enforceable contract root cause. | — |
| LYSWP2-3 | 21–25 | Informational | Fixed | Excluded: cross-chain asset-denomination/quote integration concern; the contract transfers the supplied base-unit amount. | — |
| LYSWP2-10 | 26 | Informational | Fixed | Excluded: TODO comments without an asset-loss path. | — |
| LYSWP2-11 | 27 | Informational | Acknowledged | Excluded: comment wording only. | — |
| LYSWP2-12 | 28–29 | Informational | Fixed | Excluded: equality difference in reward-timelock validation without a demonstrated loss path. | — |

## Review disclosures

- H-01 depends on a client accepting the LP's minimum-duration lock. The code
  root cause is still enforceable: both sides receive independent 15-minute
  minima with no cross-chain ordering/safety-gap invariant.
- H-02 is included despite the report's acknowledged status because the
  vulnerable snapshot accepts fee-on-transfer tokens and records more assets
  than it receives.
- H-03 covers both ignored inbound and outbound return values under one root
  cause: state proceeds after a failed token movement.
- H-04 requires a live hard fork with duplicated HTLC state. Its loss path is
  the unintended authorization of forked assets, not a claim about ordinary
  same-chain replay.
