# Initia PDF and OCR review

## Source identity

- Report: `Initia Security Review`, Pashov Audit Group.
- Review dates: June 17–23, 2025.
- Physical PDF pages and OCR records: 38 each, mapped one-to-one by exported
  `page_number`.
- OCR SHA-256:
  `7c62a967214341879f7c01a853b12efa4b307410ef85efaa14e139ff1793c65c`.
- PDF SHA-256:
  `67d7fbfadc21cbf638f7114989fde983e16c002e336bc34c6c8ef0f52c59adc0`.

## Page roles

| Physical/OCR page | Role |
|---:|---|
| 1 | Identity and date |
| 2–3 | Table of contents and finding index |
| 4 | Report introduction; explicitly describes a React SDK and a separate Router API |
| 5 | Generic severity rubric |
| 6 | Audited/fix commits and unqualified relative scope paths |
| 7 | Repository identity and report summary |
| 8–9 | Summary of all 28 findings |
| 10–11 | M-01 |
| 11–13 | M-02 |
| 13–15 | M-03 |
| 15–18 | M-04 |
| 18–19 | M-05 |
| 20 | L-01 starts; L-02 starts |
| 21 | L-02 ends; L-03 |
| 22 | L-04; L-05 starts |
| 23 | L-05 ends; L-06; L-07 starts |
| 24 | L-07 ends; L-08 starts |
| 25 | L-08 ends; L-09; L-10 starts |
| 26 | L-10 ends; L-11 starts |
| 27 | L-11 ends; L-12 starts |
| 28 | L-12 ends; L-13 |
| 29 | L-14; L-15 starts |
| 30 | L-15 body |
| 31 | L-15 ends; L-16; L-17 starts |
| 32 | L-17 ends; L-18 starts |
| 33 | L-18 body |
| 34 | L-18 ends; L-19; L-20 starts |
| 35 | L-20 body |
| 36 | L-20 ends; L-21 starts |
| 37 | L-21 ends; L-22 starts |
| 38 | L-22 ends; L-23 |

## Scope reconciliation

Page 6 lists relative paths without naming their package/repository. The first
eight entries map exactly beneath `packages/widget-react/` in the audited Git
tree: `src/components/`, `src/data/`, `src/lib/router/`, `src/pages/`,
`src/public/`, `src/styles/`, `src/console.ts`, and `src/index.ts`.

The remaining entries (`src/app/`, `src/shared/`, `src/types/`, `src/utils/`,
`constants`, `env`, `main`, and `sentry.ts`) correspond to the Router API
described on page 4, but no Router API tree exists at the report's sole audited
commit. The report therefore spans at least two application components while
providing only one repository/commit identity.

OCR text was retained verbatim. Material transcription corrections are stored
in `p2-ocr-corrections.json`; normalized conclusions use the PDF and audited
code, not corrected OCR.
