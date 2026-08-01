# P4 finding dispositions: Benqi Governance

Status: `blocked_before_code_grounding`

The report has no critical, high, or medium findings. This worksheet screens
all 21 report entries at the PDF layer only. It does not select benchmark gold:
every plausible asset-loss item remains blocked until the exact vulnerable code
is available.

| Report ID | Pages | PDF-layer disposition | Reason |
|---|---:|---|---|
| L-01 | 6–7 | Pending code grounding | Incorrect reward calculations if a permissioned configuration changes; plausible reward misallocation, but exact code and prerequisite semantics are unverified. |
| L-02 | 7 | Exclude | Incompatible setter target causes distribution DoS; report gives no concrete asset-loss path. |
| L-03 | 8 | Exclude | ERC-165 interface-reporting defect only. |
| L-04 | 8–9 | Exclude | Action-count overflow yields temporary DoS only. |
| L-05 | 9–12 | Pending code grounding | Delayed distribution can leave part of a transferred QI budget unclaimed; potential platform/user reward loss requires exact accrual and rescue-path verification. |
| L-06 | 12–13 | Exclude | Report says the system is intentionally a single-QI distributor; no supported multi-token asset-loss path. |
| L-07 | 14–15 | Pending code grounding | Buffer-window execution can skip two epochs of rewards; plausible concrete reward loss requires vulnerable-code verification. |
| L-08 | 15–16 | Pending code grounding | Asymmetric gauge removal can preserve emissions indefinitely and exhaust/misallocate QI; plausible concrete platform loss requires code verification. |
| L-09 | 16 | Pending code grounding | Gauge removal can invalidate vote weight and voter rewards; exact authorization, timing, and root cause require code verification. |
| L-10 | 16–17 | Exclude | View-function return/revert semantics; no asset-loss path. |
| L-11 | 17–18 | Pending code grounding | Invalid DAO controller configuration can skip expected rewards; plausible loss is configuration-dependent and unverified in code. |
| I-1 | 19 | Exclude | Duplicate constants/maintenance concern. |
| I-2 | 19–20 | Exclude | Generic non-standard ERC-20 transfer compatibility issue; the report does not establish such a supported reward token or concrete loss. |
| I-3 | 20 | Exclude | Test-name/documentation mismatch. |
| I-4 | 20–26 | Exclude | Report explicitly says distributions are unaffected by voter-side gauge deactivation. |
| I-5 | 26–27 | Exclude | Ineffective precision factor without a demonstrated concrete asset-loss sequence. |
| G-1 | 28 | Exclude | Gas/style only. |
| G-2 | 28 | Exclude | Gas optimization only. |
| G-3 | 28–29 | Exclude | Style/gas only. |
| G-4 | 29 | Exclude | Redundant validation/gas only. |
| G-5 | 29 | Exclude | Counter simplification/gas only. |

## Selection result

Selected findings: **none**.

Provisional code-review queue: `L-01`, `L-05`, `L-07`, `L-08`, `L-09`, and
`L-11`. These are navigation targets, not accepted findings. Their distinct
root causes, vulnerable reachability, affected assets, and direct/indirect loss
paths cannot be established without the exact audited tree.
