# Omni SolverNet C1 review

Candidate `2025-03-omni-solvernet` revision C1r1 is complete and remains **in review**. It supersedes C1 digest `832b40c860fce19aac92d4e7ce22477c175034a7d73878337629a6ffa14c804e` after the first image build exposed a one-character omission in the Foundry tarball checksum. C1r1 changes the Dockerfile checksum from the invalid 63-character `cf7e688e0c...` value to verified SHA256 `cf7e688ed0c4c48adffca788b496076e31060b67ac5afe1e43dbb5499c20c88b`; semantic findings and source evidence are unchanged. The exact vulnerable snapshot is `omni-network/omni` at `3ef37ae2704db4e1dcb8fc3f7acbb8babb543e8c`; the remediation commit is retained only as comparison evidence. Four distinct loss-of-funds findings are included (OMNI6-01 through OMNI6-04, report pages 8–14); nine availability, gas, deployment-hardening, or informational observations are excluded.

OCR and PDF provenance passed strict validation. The source PDF is the 27-page Sigma Prime report, and the immutable OCR JSONL has 27 ordered records. The report's `utils/*` scope label is normalized to the exact snapshot's singular `util/DeployedAt.sol` path. The isolated clone builds and passes 37/37 Foundry tests offline with solc 0.8.24. No report PDF or OCR JSONL is present in the candidate runtime context. No Harbor task, admission, model smoke, or external publication has been performed.

Open review risks: H-01 and H-02 rely on the pinned OmniPortal cross-contract behavior; no finding-specific exploit tests are claimed; the agent image is local-only until approval.

Approval required before C2: approve this exact candidate and review-bundle digest, naming the reviewer identity. Approval does not authorize unrelated queue changes.
