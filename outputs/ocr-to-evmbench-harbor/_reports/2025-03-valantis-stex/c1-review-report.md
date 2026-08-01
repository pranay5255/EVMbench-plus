# Candidate C1 Review Report

Candidate: `2025-03-valantis-stex`

Review-bundle digest:
`eb37343a23b3c171ccb5bcf7f24eff3079cbe29d3131cc7473cc91abe31f453d`

The digest is the SHA-256 of the exact bytes of
`c1-review-manifest.json` (11,195 bytes).

## Selected findings

| Gold ID | Report ID | Pages | Award |
|---|---|---:|---:|
| H-01 | VLTS3-5 | 10–12 | 1.0 |
| H-02 | VLTS3-13 | 13–18 | 1.0 |
| H-03 | VLTS3-3 | 19–20 | 1.0 |
| H-04 | VLTS3-9 | 21–25 | 1.0 |
| H-05 | VLTS3-14 | 26–27 | 1.0 |

`max_score = 5`.

## Validation outcome

- Structural validator: passed in the clean pinned OPD_base clone, without
  `--require-approved`.
- Semantic validation: passed; all five findings were rechecked against the
  exact PDF and vulnerable code.
- Repository validation: passed at vulnerable commit
  `25a19b663f86b53112a5e020c843904a571cc1e8`; all 14 recursive submodule
  revisions were verified.
- Agent image:
  `sha256:a8604ad62325521d2c597f46932094ae94f293b926194eba78e5ead4ba9ee9b7`.
- Offline Foundry: 102 files compiled; 34 tests passed, 0 failed, 0 skipped.
- Leakage: passed. The final rootfs and all saved layers contain zero PDFs,
  zero post-audit commit objects, zero nested Git stores, and zero candidate
  authoring artifacts or distinctive answer markers.
- Unresolved semantic or reproducibility concerns: none.

The original failed P6 reports remain preserved in the manifest. The successful
P5R/P6R reports supersede them for this exact reviewed candidate.

## Isolation and approval state

The OCR and PDF hashes are unchanged. Adjacent dirty OPD_base and
forestOfAudits checkouts are unchanged. No canonical EVMBench or Harbor state
was modified, no agent/model ran, and no candidate was admitted.

Current candidate state remains:

```yaml
state: in_review
human_approved: false
```

Admission requires an explicit statement containing the exact candidate ID,
the exact digest above, admission approval, and reviewer identity.
