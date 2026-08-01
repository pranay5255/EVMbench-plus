# P2 PDF/OCR review: `2025-10-accountable`

Status: `passed`

Review date: `2026-07-27`

The preserved 37-record OCR JSONL and the 37-page source PDF remain
byte-for-byte unchanged. Exported OCR page numbers map one-to-one to physical
PDF pages.

## Integrity results

| Check | Result |
|---|---|
| OCR JSONL SHA-256 before/after | `0c0ed8af4f1f0c90f62ea0b23e375c2aa2de2a7306941356a9dc0bf5ded28fcb` / unchanged |
| PDF SHA-256 before/after | `5ff212c2abd0c2a690914ee7ae5e48fc18cfe8cb8662afde44788bf024034e90` / unchanged |
| OCR validator | Pass: 37/37 records, 19 global checks, 1,924 record checks, zero failures |
| Physical PDF | Pass: 37 pages, unencrypted, unrotated |
| Layout text extraction | Pass: 37 page separators |
| Source path/hash agreement | Pass: all 37 OCR rows |
| Finding accounting | Pass: 33/33 report findings |

The persisted OCR validator report now uses the project-neutral schema name
`ocr_to_evmbench_harbor.ocr_validation.v1`. The corresponding validator tests
pass.

## Page-map review

Text extraction, OCR heading extraction, PDF hyperlinks, and rendered-page
inspection were used together. Rendered checks included the repository/scope
pages and finding transition pages across critical, high, medium, low,
informational, and gas sections. Shared boundary pages are intentional when
one finding ends and the next begins on the same physical page.

The authoritative 33-entry range list is stored in
`p2-pdf-validation.json`. Its severity totals are:

| Severity | Count |
|---|---:|
| Critical | 4 |
| High | 2 |
| Medium | 12 |
| Low | 5 |
| Informational | 9 |
| Gas | 1 |
| Total | 33 |

Normalized OCR/PDF text ratios for pages 6–37 are retained as diagnostics,
not pass/fail thresholds. Syntax highlighting, tables, line wrapping, and diff
markup explain the lower-layout pages; rendered inspection did not reveal a
page-identity or finding-boundary mismatch.

## OCR reconciliation

The preserved JSONL was not edited. Five PDF-grounded corrections are recorded
in `p2-ocr-corrections.json`: two full commit values recovered from page-7
hyperlinks, `unpredictable` on page 22, `Ownable2Step` on page 33, and the
single-underscore `_calculateRequiredLiquidity` identifier on page 37.

These corrections establish PDF transcription only. Identifier spelling and
finding semantics still require verification against the exact vulnerable
tree in P3.

## Exit decision

P2 passes independently of P1. This does not cure the missing repository
snapshot, establish any gold finding, authorize candidate creation, or permit
Harbor work.
