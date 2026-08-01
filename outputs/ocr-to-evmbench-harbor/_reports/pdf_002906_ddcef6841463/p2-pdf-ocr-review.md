# UFarm PDF and OCR review

## Source identity

- Report: `Security Review Report for UFarm`, Hexens, May 2025.
- Audit window: May 26–June 30, 2025.
- Physical PDF pages and OCR records: 31 each, mapped one-to-one by exported
  `page_number`.
- OCR SHA-256:
  `097be42f6831d661eb05870845f9b67b31d75051af4982aa488bd41edfe482fe`.
- PDF SHA-256:
  `f83b7a21de368b71f90138371290b2f435f72888f840b274649f793e4cb4e281`.

## Page roles

| Physical/OCR page | Role |
|---:|---|
| 1 | Cover |
| 2 | Table of contents and finding titles |
| 3 | Auditor identity and methodology |
| 4 | Executive summary |
| 5 | Scope, vulnerable commit, fixed repository/commit, and dates |
| 6–7 | Severity rubric and symbolic-code explanation |
| 8 | Findings summary: 1 critical, 3 high, 5 medium, 1 low |
| 9–11 | UFARM1-2 |
| 12–14 | UFARM1-1 |
| 15–16 | UFARM1-4 |
| 17–20 | UFARM1-9 |
| 21 | UFARM1-3 |
| 22–23 | UFARM1-6 |
| 24–25 | UFARM1-7 |
| 26–27 | UFARM1-8 |
| 28–29 | UFARM1-10 |
| 30 | UFARM1-5 |
| 31 | Closing graphic |

## Scope evidence

PDF page 5 embeds the audited source link as
`https://gitlab.com/mobileup/ufarm-digital/ufarm-evm-contracts/-/tree/aa69668de34c7bcd32cb271d082a4398d127b145`.
The report distinguishes that vulnerable commit from the fixed source link
`https://github.com/UFarmDigital/UFarm-EVM-Contracts/tree/2fc58b7b810b82a2385ea8e275665311e3b8364f`.
The PDF describes the scope as updates to the core protocol and does not list a
path allowlist. Finding paths are chiefly under
`contracts/main/contracts/pool/`, with one finding in `FundFactory.sol` and one
in `UnoswapV2Controller.sol`.

## OCR reconciliation

The OCR preserves all 10 finding boundaries and the vulnerable commit exactly.
It mis-transcribes the fixed commit and several code identifiers. The immutable
OCR was not changed; material corrections are listed in
`p2-ocr-corrections.json`. All normalized conclusions in this bundle use the
hash-verified PDF, not corrected OCR text.
