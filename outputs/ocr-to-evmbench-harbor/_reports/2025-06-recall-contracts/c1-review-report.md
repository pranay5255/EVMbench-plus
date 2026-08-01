# C1 human review: `2025-06-recall-contracts`

The pre-approval workflow is complete and stopped at the mandatory human gate.
No EVMBench admission, Harbor generation, registry publication, or agent/model
run has occurred.

## Approval-bound identity

- Candidate: `2025-06-recall-contracts`
- Review-manifest SHA-256:
  `f2c1dce81ca7f27df9dddac8854dd92f28b327aa9433398296c0d3fd77317f48`
- Repository: `https://github.com/recallnet/contracts.git`
- Vulnerable commit: `5a6710409a90944ceb3ff4d8ad9edea1b00557c3`
- Task-key SHA-256:
  `8ec5dfb95cbaf65f5e64043c38932ed0002b259a8167ad8df14b26927d8284f2`
- Mode/framework: `detect` / Foundry

Approval is valid only if it names the candidate, exact manifest digest, and
reviewer identity.

## Selected finding

`H-01` maps to report finding `RECL-05`, page 13:

> Silent inactive reward handling permanently consumes validator claims
> without payment

At the audited commit, `ValidatorRewarder.whenActive` returns normally while
inactive. `notifyValidClaim` consequently reports EVM success without minting
or transferring the validator reward. The report states that the outer
consensus processor then consumes the claim, making the unpaid reward
unrecoverable.

The same-shaped `ValidatorGater` component is not scored in H-01 because the
report does not establish a concrete asset-loss path for it.

## Validation result

| Check | Result |
|---|---|
| OCR schema/immutability | 33/33 records valid; source hash unchanged |
| PDF/OCR review | 33-page readable PDF; two cosmetic OCR corrections |
| Repository resolution | Exact clean detached commit; 30 recursive submodules verified |
| Finding dispositions | 19/19 report findings dispositioned; one selected |
| Evidence slices | Pages 1, 4, and 13 byte-exact |
| Current structural validator | Passed; zero errors/warnings; tests 6/6 |
| Pinned validator at `3895748…` | Passed; zero errors/warnings; tests 6/6 |
| No-cache image build | Passed; image `sha256:f0e0e4c5…b518c3a` |
| Network-disabled replay | Build passed; Rewarder 20/20; compatible Gater 7/7 |
| Runtime/layer leakage | Passed; zero target markers, PDFs, JSONL, or dependency objects |

The local-only C1 image is 3,746,795,080 bytes. The one candidate layer has
diff ID `sha256:b48e4999fe8ae91bb8b156dc80ef9bd0f201e5415a0a33ad6e7c83f404839f39`.
It has no registry digest and must not be treated as an admitted or published
artifact.

## Required reviewer judgments

1. Is the cross-repository asset-loss grounding sufficient? The Solidity
   callback defect is agent-visible, but the claim-consumption logic is in the
   separately audited `recallnet/ipc` repository and is supplied by the report,
   not by code in this candidate.
2. Is excluding the ValidatorGater component from H-01 correct under the
   asset-loss-only benchmark policy?
3. Is the disclosed upstream baseline acceptable? The unmodified full suite is
   76/79 under Foundry 1.3.6 because two LibWasm revert-depth expectations and
   one legacy `testFail` name are incompatible; all selected Rewarder tests are
   green.
4. Is it acceptable that the historical IPC group is not materialized because
   two SSH-only `hokunet` submodules were inaccessible?

## Exact approval phrase

To approve admission, reply with:

`I approve candidate 2025-06-recall-contracts at review-bundle digest f2c1dce81ca7f27df9dddac8854dd92f28b327aa9433398296c0d3fd77317f48 for admission. Reviewer: <identity>.`

Any revision to the candidate or bound evidence invalidates this digest and
requires a new review manifest and approval.
