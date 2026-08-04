# P2 PDF/OCR review — Algebra ALM (`pdf_003345_a305f8485f3a`)

## Source identity

| Field | Value |
|---|---|
| PDF | `/home/experiments_base/smart-contract-data/crawlers/output/repos/audit_repos/audits_public/Algebra Finance/Algebra ALM/Algebra ALM Security Audit Report.pdf` |
| PDF SHA-256 | `810310a7d0bc20feb362250ebef10fd22946436fdd1dc998431be2a490819856` |
| Physical pages (PyMuPDF) | 35 |
| OCR JSONL | `outputs/evmbench_task_batch/extracted_pages/pdf_003345_a305f8485f3a.jsonl` |
| OCR SHA-256 | `cebf3de80fc6909d3af0c82800c8ce86e77401726a1b29b2df46f266093f9525` |
| OCR records | 35 (`1..35`) |
| Report | MixBytes — Algebra ALM Security Audit Report — 19 December 2025 |

Gate 1 structural OCR validation: PASS (19 global / 1820 record checks).
Gate 2 PDF hash and page-count reconciliation: PASS.

## Page roles (selected)

| Pages | Role | Notes |
|---:|---|---|
| 1 | identity | Cover |
| 2–3 | summary | TOC of M-1 and L-1…L-17 |
| 4–5 | non_finding | Executive summary / notes |
| 6–7 | scope | File table + Versions Log commits; PDF hyperlinks name both repos |
| 8–10 | non_finding | Methodology / risk taxonomy |
| 11–12 | summary | Findings status table |
| 13–14 | finding (plugin) | M-1 start / L-1 |
| 15–34 | findings | L-* bodies |
| 23–24 | finding (vault) | L-7 donation/rounding theft (selected) |
| 35 | non_finding | About MixBytes |

## OCR corrections used for authoring (not applied to JSONL)

Immutable OCR was left unchanged. PDF/text extraction and hyperlinks corrected:

1. **Repository URLs** are not present as plain text in OCR; they come from PDF
   link annotations on pages 6–7:
   - `https://github.com/cryptoalgebra/AlmVault/blob/57d820afa1d58bf89073e668f5608942d90188c7/...`
   - `https://github.com/cryptoalgebra/plugins-monorepo/blob/6a5bcc44abfb90c3edb05bbea7efec233b5bd257/...`
2. **Vault Versions Log commits** (PDF text extraction):
   - Initial ALM Vault: `57d820afa1d58bf89073e668f5608942d90188c7`
   - Re-audit ALM Vault: `d637339f968d67f175e8cb56ce3ae54a69bdefee`
3. OCR on page 7 garbled several hex digits (`afald` vs `afa1d`, truncated
   plugin hashes). PDF extraction + live Git objects are authoritative.
4. L-7 client fix commit from PDF page 24:
   `9f5f362a3723e9ec6fe8686fd30a22948653e1d8`.

## Task-group decision

The single PDF produces **two** repository task-group keys (AlmVault vs
plugins-monorepo). Per reference 6, this candidate admits only the vault
snapshot. Plugin findings are dispositioned as out-of-group, not selected here.
