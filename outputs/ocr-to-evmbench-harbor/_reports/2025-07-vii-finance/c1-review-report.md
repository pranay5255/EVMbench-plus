# C1 human review: `2025-07-vii-finance`

The pre-approval workflow is complete and stopped at the mandatory human gate.
No EVMBench admission, Harbor generation, registry publication, or agent/model
run has occurred.

## Approval-bound identity

- Candidate: `2025-07-vii-finance`
- Review-manifest SHA-256:
  `4c2d5501ea684386b006267e4b85af72377a8b8289fa8b8f8596b3410e4e7840`
- Repository: `https://github.com/kankodu/vii-finance-smart-contracts.git`
- Vulnerable commit: `2a3a72c675a580dcdeb2f7d733d40c6bfb1b3dc7`
- Task-key SHA-256:
  `3950493077d13cc7943df7cfd5731a6194b89c4ebb5b1d22d01b93d63655bd48`
- Mode/framework/policy: `detect` / Foundry / `loss_of_assets`

Approval is valid only if it names the candidate, exact manifest digest, and
reviewer identity.

## How OCR evidence is used

The immutable 36-record OCR JSONL is the primary page-indexed evidence. The
candidate includes byte-exact slices for scope and repository pages 3–4 and
finding pages 14–29. Each selected finding cites those OCR artifacts; the PDF
and exact source snapshot were used to correct OCR transcription errors, not to
replace the OCR evidence.

Documented corrections include `tokensDived`/`tokenUsed` to `tokensOwed`,
`ERC8909` to `ERC6909`, the PDF hyperlink's full repository commit, and the
M-1 fix commit that OCR shortened incorrectly. The source OCR hash remained
`a7f39dffc24729be5272933d8786ffd2eed1eea631caad0ab32ae6e558006d43`
before and after processing.

## Selected findings

| Candidate | Report | Pages | Asset-loss root cause |
|---|---|---:|---|
| `H-01` | `H-1` | 14–20 | V4 partial unwrap pays fee credits without decrementing them, enabling reuse against other holders' real fee assets. |
| `H-02` | `H-2` | 21–23 | Liquidation normalization uses global token supply instead of the sender's balance, allowing excess collateral seizure or blocked liquidation. |
| `H-03` | `M-1` | 24–25 | Full unwrap bypasses V4 fee settlement and can permanently strand accrued LP fees after the final holder exits. |
| `H-04` | `M-2` | 25–29 | Floor rounding can transfer zero units of valuable residual collateral, directly underpaying a partial liquidator. |

All 10 report findings were dispositioned. Critical `C-1` is the report's
composition of H-1, H-2, and L-2 behavior, so it is split and merged into
H-01/H-02 rather than double-scored. L-1, L-2, L-3, I-1, and I-2 are excluded
under the loss-of-assets policy for the reasons bound in the manifest.

## Validation result

| Check | Result |
|---|---|
| OCR schema/immutability | 36/36 records valid; 19 global and 1,872 record checks; source hash unchanged |
| PDF/OCR review | Readable, unencrypted 36-page PDF; corrections documented separately |
| Repository resolution | Exact clean detached commit; seven scoped files and required submodule heads verified |
| Finding dispositions | 10/10 report findings dispositioned; four selected |
| Evidence slices | Pages 3–4 and 14–29 are byte-exact OCR rows |
| Offline baseline | 183 Solidity files compiled; 11/11 non-RPC tests passed |
| Current structural validator | Passed; zero errors/warnings; validator tests 6/6 |
| Pinned validator at `3895748…` | Passed; zero errors/warnings; validator tests 6/6 |
| No-cache image build | Passed; image `sha256:0292eb58…c3c418` |
| Network-disabled replay | Exact HEAD/clean status passed; build passed; tests 11/11 |
| Candidate-layer leakage | Zero PDFs, JSONL, target markers, or PDF signatures |

The local-only C1 image is 4,265,042,400 bytes. Its candidate layer has diff ID
`sha256:0901a722533c9f08069bd3feed17bc0adae4ebc038ee9a7ab781074c0820b426`.
It has no registry digest and must not be treated as admitted or published.

## Required reviewer judgments

1. Is splitting composite Critical C-1 into H-01 and H-02, without a separate
   C-1 score, the correct non-duplicative treatment?
2. Are L-2's zero-balance enrollment and its liquidation consequence correctly
   excluded as dependent on H-02's same root cause and remediation?
3. Is the unlicensed (`NOASSERTION`) public repository acceptable for this
   benchmark admission?
4. Is the disclosed dependency boundary acceptable: one unreachable optional
   Redstone gitlink was not substituted, while the exact audited import graph
   compiled and the relevant non-RPC tests passed offline?
5. Is the lack of mainnet-fork and exploit-specific tests acceptable given the
   code-grounded findings, exact remediation diffs, and green baseline?

## Exact approval phrase

To approve admission, reply with:

`I approve candidate 2025-07-vii-finance at review-bundle digest 4c2d5501ea684386b006267e4b85af72377a8b8289fa8b8f8596b3410e4e7840 for admission. Reviewer: <identity>.`

Any revision to the candidate or bound evidence invalidates this digest and
requires a new review manifest and approval.
