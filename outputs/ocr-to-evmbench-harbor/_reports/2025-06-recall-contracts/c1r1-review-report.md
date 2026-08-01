# C1R1 human review: `2025-06-recall-contracts`

The detect-only revision is complete and stopped at the mandatory human gate.
The prior C1 approval and isolated admission are superseded because the
user-requested scope correction changed a review-bound Dockerfile byte. The
canonical EVMBench checkout was not written, and no Harbor task, registry
publication, or agent/model run occurred.

## Approval-bound identity

- Candidate: `2025-06-recall-contracts`
- C1R1 review-manifest SHA-256:
  `444ee75d07d977f33ed4b208210023f01d7d4b0b5025b2f3554e5d2132adc7ef`
- Repository: `https://github.com/recallnet/contracts.git`
- Vulnerable commit: `5a6710409a90944ceb3ff4d8ad9edea1b00557c3`
- Task-key SHA-256:
  `8ec5dfb95cbaf65f5e64043c38932ed0002b259a8167ad8df14b26927d8284f2`
- Mode/framework: `detect` / Foundry

Approval is valid only if it names the candidate, exact C1R1 manifest digest,
and reviewer identity.

## Selected finding

`H-01` maps to report finding `RECL-05`, page 13:

> Silent inactive reward handling permanently consumes validator claims
> without payment

At the audited commit, `ValidatorRewarder.whenActive` returns normally while
inactive. `notifyValidClaim` consequently reports EVM success without minting
or transferring the validator reward. The report states that the outer
consensus processor then consumes the claim, making the unpaid reward
unrecoverable.

The `ValidatorGater` component is excluded from scoring and selected-path test
execution because the report does not establish a concrete asset-loss path for
it.

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
| No-cache image build | Passed; image `sha256:7d07380c…01e372c` |
| Network-disabled replay | Build passed; selected Rewarder tests 20/20; Gater tests 0 |
| Runtime/layer leakage | Passed; zero target markers, PDFs, JSONL, or dependency objects |

The C1R1 image is local-only, 3,746,802,169 bytes, and has candidate-layer
diff ID
`sha256:ccdb007a1004d7a1a12d0bc5b73f07bd08977af8b9016cd69150d121d2eee764`.
It has no registry digest and is not an admitted or published artifact.

## Required reviewer judgments

1. Is the cross-repository asset-loss grounding sufficient? The Solidity
   callback defect is agent-visible, but the claim-consumption logic is in the
   separately audited `recallnet/ipc` repository and is supplied by the report.
2. Is excluding `ValidatorGater` correct under the asset-loss-only policy?
3. Is the disclosed upstream baseline acceptable? The full suite is 76/79
   under Foundry 1.3.6 due three compatibility failures, while the selected
   Rewarder suite is 20/20.
4. Is it acceptable that the IPC group is not materialized because two
   SSH-only `hokunet` submodules were inaccessible?

## Exact approval phrase

To approve admission, reply with:

`I approve candidate 2025-06-recall-contracts at review-bundle digest 444ee75d07d977f33ed4b208210023f01d7d4b0b5025b2f3554e5d2132adc7ef for admission. Reviewer: <identity>.`

Any revision to the candidate or bound evidence invalidates this digest and
requires a new review manifest and approval.
