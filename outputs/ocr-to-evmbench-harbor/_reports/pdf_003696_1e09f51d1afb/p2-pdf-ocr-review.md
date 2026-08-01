# EigenLayer EigenDA PDF and OCR review

## Source identity

- Report: `EigenDA Proxy Secure Integration Security Assessment Report`,
  Sigma Prime for Layr Labs, version 2.0, October 2025.
- Physical PDF pages and OCR records: 33 each, mapped one-to-one by exported
  `page_number`.
- OCR SHA-256:
  `b6e57d6e6cf6a894a6f9d015170621861b3bc82091e0579efdf7cfa4d41b7686`.
- PDF SHA-256:
  `2900c32ac36fb78949c11cc620c68efe453b411d021a2f09665c91dcb00b42fb`.

## Page roles and finding boundaries

| Physical/OCR page | Role |
|---:|---|
| 1 | Cover, client, report title, version, and date |
| 2 | Contents and finding-title index |
| 3 | Introduction and EigenDA write/read-path overview |
| 4 | Repository, vulnerable/fixed commits, exact scope, exclusions, and approach |
| 5 | Coverage limitations and severity counts |
| 6 | Detailed-findings introduction |
| 7 | Sixteen-item summary table with severity and resolution status |
| 8–9 | EDA-01 |
| 10–11 | EDA-02 |
| 12–13 | EDA-03 |
| 14–15 | EDA-04 |
| 16 | EDA-05 |
| 17–18 | EDA-06 |
| 19 | EDA-07 |
| 20–21 | EDA-08 |
| 22 | EDA-09 |
| 23 | EDA-10 |
| 24 | EDA-11 |
| 25 | EDA-12 |
| 26 | EDA-13 |
| 27 | EDA-14 |
| 28 | EDA-15 |
| 29–31 | EDA-16 and its five general comments |
| 32 | Severity-classification appendix and references |
| 33 | Trailing blank page |

The executive summary and summary table agree on 16 items: one Medium, seven
Low, and eight Informational; no Critical or High item appears. The item IDs,
titles, severities, statuses, and page boundaries are complete.

## Scope evidence

PDF page 4 identifies `Layr-Labs/eigenda`, audited short commit `066f8ef`, and
fixed short commit `794c356`. GitHub and the Git objects resolve these to:

- vulnerable commit `066f8ef4f93bb8ce196555904e89adf7ef50e57f`;
- fixed commit `794c356269b2e9559b6d43e4b21dee7c45eb354b`.

The report says the review was strictly limited to `api/clients/*`,
`api/proxy/*`, and `contracts/src/integrations/cert/*`, with
`contracts/src/integrations/cert/legacy/*`, third-party libraries, and
dependencies excluded. The exact vulnerable tree contains all three included
areas. EDA-14 names only paths outside that strict scope. EDA-06 partly names
`contracts/src/core/PaymentVault.sol`, also outside scope, but its Go client
mechanism is inside `api/clients/*`. These report/scope inconsistencies are
recorded rather than silently broadening the task.

## OCR reconciliation

OCR preserves the page count, short commits, scope prefixes, severity counts,
all 16 finding boundaries, and the overall descriptions. It corrupts the
repository owner (`Lyr-Labs`), `RetrieveBlobChunks`, and numerous code tokens,
especially the EDA-13 route snippet and EDA-16 examples. Exact values and all
semantic decisions therefore come from the hash-verified PDF and exact Git
tree. The immutable OCR was not edited; material corrections are recorded in
`p2-ocr-corrections.json`.
