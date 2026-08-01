# P2 PDF and OCR review — Hemi Labs VUSD

Status: **PASS**

## Source identity

- PDF:
  `/home/experiments_base/smart-contract-data/crawlers/output/repos/audit_repos/audit-reports/Hemi_Labs_Final_Audit_Report.pdf`
- SHA-256:
  `76d151f58c3edb5688802c8bd5dbd3727bb3b4a0d3ecc858b4b88e457a8be6e3`
- Physical pages: `32`
- OCR:
  `/home/experiments_base/OPD_base/outputs/evmbench_task_batch/extracted_pages/pdf_002969_2a929a776caf.jsonl`
- OCR SHA-256:
  `a79ba90ae9ed42bf8d7e620bbb06ea36799f13b5f33dcefc36b477614ff21182`
- OCR records: `32`, ordered physical pages `1..32`

The PDF is readable, unencrypted, and exactly matches the preserved inventory
checksum and page count. OCR validation passed 19 global checks and 1,664
record checks with no failures.

## Report identity and scope

CredShields audited Hemi Labs' VUSD contracts from March 4–7, 2025 and retested
on March 10. Physical page 6 defines the in-scope asset as:

```text
https://github.com/hemilabs/vusd-stablecoin/tree/54f9f235f26df813152b3d3235e7f4373ce473b6
```

The physical PDF and the repository object database resolve this commit
exactly. OCR inserts an extra `3` after `152b` in displayed links; that OCR
string is preserved verbatim in the evidence slice but is not used as the
snapshot identity.

## Page map

| Physical page(s) | Role |
|---:|---|
| 1 | identity and report date |
| 2–3 | table of contents |
| 4–5 | executive summary and security posture |
| 6 | audited repository and exact commit scope |
| 7–9 | methodology and generic severity definitions |
| 10–11 | findings overview and summary only |
| 12–14 | generic SWC checklist |
| 15 | remediation summary |
| 16 | Bug ID #1; selected as H-01 |
| 17 | Bug ID #2; selected as H-02 |
| 18 | Bug ID #3; selected as H-03 |
| 19–20 | Bug ID #4; page 20 continues the retest comment |
| 21–22 | Bug ID #5 |
| 23–24 | Bug ID #6 |
| 25–26 | Bug ID #7 |
| 27–28 | Bug ID #8 |
| 29 | Bug ID #9 |
| 30 | Bug ID #10 |
| 31–32 | disclosure and back cover |

Every selected finding uses its physical start/end page. Summary pages and OCR
chunk boundaries are not used as gold evidence.
