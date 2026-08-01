# P2 PDF/OCR review: Benqi Governance

Status: `passed_source_document_review`

Review date: `2026-07-31`

The preserved 29-record OCR JSONL and the 29-page source PDF remain
byte-for-byte unchanged. Exported OCR page numbers map one-to-one to physical
PDF pages.

## Integrity results

| Check | Result |
|---|---|
| OCR JSONL SHA-256 before/after | `2de66fc23d5216db39fa0d492cebf886a57e9e2a7abd0ba81d87f2dd5b024522` / unchanged |
| PDF SHA-256 before/after | `dd1ac726e8088bda57191043993fd9eba126f358d44156344d2ed3b56bc48128` / unchanged |
| OCR validator | Pass: 29/29 records, 19 global checks, 1,508 record checks, zero failures |
| OCR validator unit tests | Pass: 3/3 |
| Physical PDF | Pass: 29 pages, unencrypted, unrotated |
| Layout text extraction | Pass: 29 page separators |
| Source path/hash agreement | Pass: all 29 OCR rows |
| Finding accounting | Pass: 21/21 report findings |

## Authoritative identity and scope

The PDF annotations—not the truncated OCR table—identify:

- repository: `https://github.com/aragon/benqi-governance`;
- vulnerable commit: `ded42b671f112eef318482a8c9f10329d0aeef65`;
- ten in-scope Solidity files under `src/contracts/`, recorded in
  `p2-pdf-validation.json`;
- report date/version: November 10, 2025 / 2.0.

The report contains 11 low-risk, 5 informational, and 5 gas findings. It
contains no critical, high, or medium finding. Shared boundary pages in the
21-entry range map are intentional where one finding ends and the next begins
on the same physical page.

## Side-by-side reconciliation

Layout text, OCR blocks, PDF hyperlinks, and rendered pages were inspected
together. Rendered inspection covered the scope and commit pages plus all pages
that describe a plausible reward-token or voting-reward loss path. The OCR
correctly preserves page identity and finding transitions but is not safe as
code: examples include the case error in `BenqiEcosystemModule.sol`, the
truncated commit, and arithmetic/identifier corruption in Solidity snippets.
The immutable JSONL was not edited; PDF-grounded corrections are stored in
`p2-ocr-corrections.json`.

## Exit decision

P2 passes independently of repository recovery. It establishes the report's
intended repository, commit, scope, and page map, but it does not establish a
checkout, framework, vulnerable code semantics, gold findings, or permission to
create a candidate.
