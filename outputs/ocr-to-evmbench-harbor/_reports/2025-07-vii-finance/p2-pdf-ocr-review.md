# PDF and OCR review — VII Finance

The immutable 36-row OCR export passed every schema, ordering, duplicate-field,
page-coverage, provenance, and input-immutability check. The source PDF hash
matches all OCR records and the selected-20 inventory, and `pdfinfo` reports 36
physical pages.

The OCR was used to map and preserve page-bounded evidence. The PDF was used to
resolve visual text, hyperlinks, symbols, and code identifiers that OCR did not
reliably preserve. The exact vulnerable checkout was used to decide semantics.

## Page map

| Exported page(s) | Role | Review result |
|---|---|---|
| 3 | Scope | Seven Solidity paths, visually verified and present in the exact tree |
| 4 | Repository and commit | PDF hyperlinks resolve `kankodu/vii-finance-smart-contracts@2a3a72c675a580dcdeb2f7d733d40c6bfb1b3dc7` |
| 5 | Summary | Ten report findings; used only as a cross-check |
| 6–13 | C-1 | Composite liquidation chain; split into underlying root causes, not separately scored |
| 14–20 | H-1 | Selected as `H-01` |
| 21–23 | H-2 | Selected as `H-02` |
| 24–25 | M-1 | Selected as `H-03`; page 25 also begins M-2 |
| 25–29 | M-2 | Selected as `H-04` |
| 30–32 | L-1 | Excluded: report identifies no clear material or profitable attack |
| 33 | L-2 | Excluded as an H-2-dependent symptom with no independent asset-loss root cause |
| 33–35 | L-3 | Excluded: empty zero-liquidity NFT reuse has no established asset value |
| 36 | I-1 and I-2 | Excluded: caller-controlled revert and duplicate import |

## OCR corrections and boundaries

- Page 4 exposes only the visible short SHA in OCR. The PDF hyperlink supplies
  the full vulnerable SHA; it resolves to a real commit whose root tree is
  `93e281561e07ae50cbbf4d08eef6c2d7a5fb6f48`.
- Code identifiers were normalized only in authored findings after comparison
  with the PDF and source. Original OCR rows remain byte-for-byte unchanged.
- Page 25 legitimately appears in both M-1 and M-2 evidence slices because it
  concludes M-1 and starts M-2. No OCR chunk boundary was used as a finding
  boundary.

The source PDF remains outside the candidate, image build context, and any
future Harbor tree.
