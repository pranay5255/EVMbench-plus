# Mellow PDF/OCR review

The source is the 25-page Nethermind Security report **NM-0587 Mellow
Protocol**, finalized September 3, 2025. The PDF and all 25 OCR records bind to
PDF SHA-256 `13a18507a8edf3db6e578788d853b76acc3935b1bac37ccc40b6c377f030ceab`.
The OCR JSONL passed strict validation with 25 ordered records and no global or
per-record failures; it was unchanged before and after review.

Every PDF page was rendered and visually inspected. Candidate scope evidence
uses exported pages 3-5. Page 3 identifies the repository and headline
initial/final commits; pages 4-5 enumerate 75 audited Solidity files. Finding
evidence uses exported page 9, which contains all of report finding 6.1.

The PDF's hyperlinks resolve a subtle snapshot issue that the OCR text cannot:
`src/oracles/OracleHelper.sol` and both OracleHelper finding links target
commit `60c462d6b006b19790b07c009b7a48aa3bcb3e96`.
`OracleHelper.sol` is absent from headline initial commit `69413d54...`.
Commit `60c462d6...` is a descendant of the headline initial commit and an
ancestor of final remediation commit `72f689f9...`; it is the only report-linked
snapshot that contains the full 75-file audited scope and both high findings.

The report has five findings: two High and three Informational. Only 6.1 is
admitted under `loss_of_assets`. Finding 6.2 grounds stale prices and denial of
service but does not provide a concrete asset-transfer/loss sequence. Findings
6.3 and 6.4 are documentation defects. Finding 6.5 is an acknowledged encoding
risk that the client states is inapplicable under static naming assumptions.

OCR mistakes and missing hyperlink semantics were not written back to the
immutable source. Corrections are recorded in `p2-ocr-corrections.json` and all
candidate OCR excerpts are byte-exact source rows.
