# P2 PDF and OCR review: `2025-01-burve`

Status: passed.

The immutable 28-line OCR JSONL and the 28-page PDF identify the same source:

- PDF SHA-256: `9331ef94ce1ae3fecce225d5aa49a08583a66e625fd728463af4ca15b7135404`
- OCR SHA-256: `a6ede0f0946928351257c3b0800f75118d716d49438a99aaa287877782b6657a`
- Report: Pashov Audit Group, *Burve Security Review*
- Audit period: January 29 through February 6, 2025

Every PDF page was rendered and reviewed against the corresponding OCR record.
The PDF annotations on physical page 6 give vulnerable commit
`f0597768fee2d00c17429941f4721475e1ca5723` and fixes commit
`e89ebff2c7daafc98e94c66e4273e4c366949c76`. Physical page 7 gives
`https://github.com/itos-finance/Burve`.

The report contains 20 findings: C-01 through C-04, H-01 through H-03, M-01
through M-05, and L-01 through L-08. Finding boundaries use physical PDF page
numbers. C-03 evidence is limited to pages 13 and 14 because page 15 begins
C-04 after a short C-03 recommendation; the pinned source supplies the missing
authorization detail without mixing two finding slices.

OCR errors are navigation issues, not gold evidence. In particular, OCR
corrupts some scope names on page 6, code punctuation in C-01, and multiple
Solidity identifiers in the C-03 PoC. The candidate preserves the original OCR
lines byte-for-byte and records corrections separately.
