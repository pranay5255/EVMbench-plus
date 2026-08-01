# P3 PDF/OCR Review — `2025-03-valantis-stex`

Status: passed

Review timestamp: `2026-07-25T12:25:48Z`

This is host-side Gate 2 evidence only. It verifies the original report and its
page boundaries; it does not ground findings against vulnerable code, create a
candidate, or authorize admission.

## Source resolution and integrity

All 38 populated `raw_record.source_abs_path` values agree on:

`/home/experiments_base/smart-contract-data/crawlers/output/repos/audit_repos/Smart-Contract-Review-Public-Reports/valantis-mar-25(Final).pdf`

The first permitted resolution method therefore succeeded. The
`source_rel_path` and discovery fallbacks were not needed.

| Property | Expected | Observed | Result |
|---|---|---|---|
| PDF SHA-256 | `64bf545adb3699eed16cd21abb0d6db6a651ca273e2992a02122825ec61966a7` | same | pass |
| Physical pages | 38 | 38 | pass |
| OCR exported pages | `1..38` | `1..38`, ordered and contiguous | pass |
| Encryption | readable/unencrypted | unencrypted; full text extraction succeeded | pass |
| Full text extraction | 38 physical pages | 39,260 bytes and 38 form feeds | pass |
| OCR SHA-256 after review | `10dc7a85ff63d44fab604ffdcec2f47b22ad8abcdfea1973a553ff5c88f0268d` | same | pass |

The PDF is A4, unrotated, 13,601,799 bytes, and PDF version 1.7.

## Side-by-side method

For page 5 and pages 10–27, the OCR layout tags were removed in memory and the
visible OCR text was compared with `pdftotext -layout` output from the same
physical page. Every OCR `page_number` footer equals both the printed PDF
footer and the physical page index. Lowercase alphanumeric sequence similarity
is between `0.989883` and `1.000000`; the differences were inspected as OCR
transcriptions rather than silently normalized.

Host-only page renders were kept under
`/tmp/valantis-ocr-harbor.iZKXoT/p3-review`. The original PDF, extracted PDF
text, and renders were not copied into `task_dir`, the output root, a
candidate, a Docker context, EVMBench, Harbor, or an image build context.

## Scope page

Physical/exported page 5 shows:

- repository:
  `https://github.com/ValantisLabs/valantis-stex/`;
- vulnerable commit:
  `25a19b663f86b53112a5e020c843904a571cc1e8`;
- fixed commit:
  `95122c7693f9516385aef330ef36bb1ccec2cb94`.

The vulnerable commit is legible and agrees with OCR. The repository casing and
fixed commit require the corrections below. The fixed commit is PDF-confirmed
at P3; existence in Git is deliberately deferred to P4.

## Finding-page reconciliation

| PDF/OCR pages | Boundary evidence | Reconciled report ID | Severity shown |
|---|---|---|---|
| 10–12 | ID/title starts on 10; impact finishes on 12; next ID starts on 13 | `VLTS3-5` | Critical |
| 13–18 | ID/title starts on 13; proof code finishes on 18; next ID starts on 19 | `VLTS3-13` | Critical |
| 19–20 | ID/title starts on 19; code finishes on 20; next ID starts on 21 | `VLTS3-3` | High |
| 21–25 | ID/title starts on 21; proof code finishes on 25; next ID starts on 26 | `VLTS3-9` | High |
| 26–27 | ID/title starts on 26; code finishes on 27; next ID starts on 28 | `VLTS3-14` | Medium |

These ranges use printed PDF/exported page numbers, not OCR response-chunk
boundaries. No extra context page is needed for any of the five ranges.

## Recorded OCR corrections

The original JSONL remains byte-for-byte unchanged.

| Page | OCR | PDF-confirmed reading | Follow-up |
|---:|---|---|---|
| 5 | `ValantisLabs/valantis-steX` | `ValantisLabs/valantis-stex` | Normalize repository identity in P4. |
| 5 | `95122c7693f9516385aef330ef36bb1cece2cb94` | `95122c7693f9516385aef330ef36bb1ccec2cb94` | Confirm commit object in Git during P4. |
| 10 | `VLTS3-S` | `VLTS3-5` | Use PDF report ID. |
| 13 | `VLTS3-i3` | `VLTS3-13` | Use PDF report ID. |
| 13 | `src/stHYPEWithdrawalModule.solutpdate#L431-L475` | `src/stHYPEWithdrawalModule.sol:update#L431-L475` | Confirm path/symbol in vulnerable code during P4. |
| 10–12 | `TokenI`/`TokenO`, `unstateToken0Reserves`, and related digit/letter substitutions | `Token1`/`Token0`, `unstakeToken0Reserves` | Confirm exact code identifiers during P4. |
| 14, 17, 18, 20, 22, 24, 27 | isolated code-token substitutions | PDF shows `safeTransferFrom`, `isZeroToOne`, `MockStHype`, `ILendingModule`, `stHYPEWithdrawalModule__claim_cannotYetClaim`, `withdrawalModule.update`, and `_amount0Min` | Confirm exact code identifiers during P4. |

Minor punctuation, typographic-apostrophe, and layout differences are not
semantic corrections. Where the report itself contains a spelling variation,
the PDF was transcribed as-is; vulnerable code becomes authoritative in P4.

## Gate result

Gate 2 passes: one exact-checksum, readable 38-page PDF is resolved; all 38
exported OCR pages reconcile one-to-one with physical pages; page 5 and pages
10–27 were reviewed; the five finding ranges are exact; corrections are
recorded without rewriting OCR; and no PDF-derived material entered an
agent-visible or build context.
