# Agora StableSwap PDF/OCR review

The source PDF and every preserved OCR row were reviewed side by side using
exported `page_number` values. The PDF is the semantic source of truth; the OCR
remains byte-for-byte unchanged and is navigation evidence only.

## Verified identity and scope

- Report: Agora StableSwap Security Review, Pashov Audit Group, June 5–11 2025.
- Repository named by the PDF:
  `https://github.com/amphora-atlas/stable-swap-dev`.
- Vulnerable review commit:
  `1dedf62430e2fcf164a807f95c80c12615bad135`.
- Separate fixes-review commit:
  `0b424f359bc22a80f681a92440cf5746e5b7dcf8`.
- In-scope contracts: `AgoraStableSwapAccessControl`,
  `AgoraStableSwapFactory`, `AgoraStableSwapPair`,
  `AgoraStableSwapPairConfiguration`, and `AgoraStableSwapPairCore`.
- Framework indicated by the report snippets: Solidity 0.8.28 and Foundry.
- Report inventory: one Medium and fifteen Low findings.

The commit, repository, scope, and counts above were checked against rendered
PDF pages 6 and 7, not inferred from OCR alone.

## Exported-page map

| Exported page(s) | Role | Evidence boundary |
|---:|---|---|
| 1 | identity | cover, auditors, report dates |
| 2–3 | summary | contents and finding-page index |
| 4 | identity | project/repository description |
| 5 | non-finding | impact and likelihood taxonomy |
| 6 | scope | vulnerable/fixed commits and five in-scope contracts |
| 7 | identity/summary | repository URL, protocol type, 16-item count |
| 8–9 | summary | M-01 and L-01–L-15 inventory/statuses |
| 10–11 | finding | M-01 |
| 12 | finding | L-01; L-02 begins |
| 13 | finding | L-02 ends; L-03 begins |
| 14 | finding | L-03 ends; L-04; L-05 begins |
| 15 | finding | L-05 ends; L-06; L-07 begins |
| 16 | finding | L-07 ends; L-08 begins |
| 17 | finding | L-08 ends; L-09 begins |
| 18 | finding | L-09 ends; L-10 begins |
| 19 | finding | L-10 ends; L-11 begins |
| 20 | finding | L-11 ends; L-12 begins |
| 21 | finding | L-12 ends; L-13 begins |
| 22–24 | finding | L-13 body/test ends; L-14 begins on 24 |
| 25 | finding | L-14 ends; L-15 begins |
| 26–29 | finding | L-15 code and proof-of-concept continuation |

## Review result

The PDF/OCR comparison supports a single intended task identity under
`loss_of_assets`, but it does not prove the Git snapshot or any finding. The
OCR contains material corruption in formulas, identifiers, and proof-of-concept
code; representative corrections are recorded in
`p2-ocr-corrections.json`. No correction was written back to the OCR JSONL.

Finding promotion is blocked at repository Gate 3 because the exact vulnerable
commit cannot be recovered. Report-level asset-loss candidates and exclusions
are recorded separately without treating them as code-grounded gold.
