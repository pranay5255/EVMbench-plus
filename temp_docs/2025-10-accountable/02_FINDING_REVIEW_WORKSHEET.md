# Accountable finding review worksheet

Status: `P2_page_map_complete_P3_code_grounding_blocked`

This worksheet accounts for all 33 PDF findings. It is not gold data. Every
disposition, affected path, exploit sequence, and deduplication decision must
be re-evaluated against detached vulnerable commit
`fc43546fe67183235c0725f6214ee2b876b1aac6`.

P2 reconciled the page references below against the hash-verified physical
PDF and recorded them in `p2-pdf-validation.json`. They are exported
OCR/physical PDF page numbers. A page
may support two findings when the next heading starts partway through that
page; later evidence slicing may therefore legitimately include the same
byte-exact JSONL row in two finding slices.

The page map is complete, but all dispositions remain preliminary because the
exact vulnerable repository snapshot required for P3 is unavailable.

## Disposition vocabulary

- `candidate`: the PDF describes a concrete asset, interest, fee, debt, or
  insolvency path; retain for exact-code review.
- `hold`: economic relevance, reachability, permanence, or deduplication is
  unresolved; do not include or exclude yet.
- `exclude`: the PDF describes compliance, best practice, metadata,
  availability, script hygiene, gas, or another issue without a sufficiently
  concrete detect-mode asset-loss path.

All statuses remain provisional until repository grounding.

## Critical and high

| Report ID | Pages | Preliminary status | PDF-grounded economic question |
|---|---:|---|---|
| C-1 | 9–10 | hold | Does deletion of the queue head create genuinely permanent asset lock with no recovery/upgrade path, or availability-only failure? |
| C-2 | 10–11 | hold | Does cancellation de-synchronization permanently strand user claims, and is it distinct from C-1/C-3 in vulnerable code? |
| C-3 | 12 | hold | Does a pending async cancellation cause only interruptible queue DoS, or unrecoverable withdrawal loss? |
| C-4 | 12–14 | candidate | Stale `totalValue` after partial fulfillment appears to inflate later redemption value and directly overpay an attacker from vault assets. |
| H-1 | 15 | candidate | Ignoring `RequestPrice` may underpay a redeemer after a price decrease; verify attacker/control assumptions and distinctness from C-4/M-09. |
| H-2 | 15–17 | candidate | Principal-only repayment appears to switch the loan to `Repaid` and forgive accrued interest owed to LPs and fee recipients. |

## Medium

| Report ID | Pages | Preliminary status | PDF-grounded economic question |
|---|---:|---|---|
| M-01 | 18 | exclude | Transfer-restriction bypass is a KYC/throttle policy failure; no independent asset theft is established in the PDF. |
| M-02 | 19 | exclude | Missing transfer-whitelist enforcement is a policy/compliance defect without a direct asset-loss sequence. |
| M-03 | 19–20 | exclude | Depositing for non-KYC receivers bypasses onboarding policy but does not itself steal or destroy assets. |
| M-04 | 20 | candidate | A manager can choose an arbitrary approved `provider` and pull that user's tokens to cover a default. |
| M-05 | 21–22 | candidate | Manual/instant fulfill paths appear to create claimable redemptions without reserving assets, causing oversubscribed claims and possible insolvency/fairness loss. |
| M-06 | 22–25 | candidate | Full-term share-burn pricing appears to reward early claimers and shift default shortfall to later LPs. |
| M-07 | 25–26 | candidate | Open-term performance and establishment fees appear configured but never charged, causing protocol/manager revenue loss. |
| M-08 | 26 | hold | Repeatedly resetting delinquency may avoid penalties and weaken lender protection, but the design is acknowledged and concrete loss/reachability need code review. |
| M-09 | 26 | candidate | A requester may front-run default at the pre-default request price and push the loss to remaining LPs; verify merge with C-4/H-1. |
| M-10 | 26–27 | candidate | A third-party deposit immediately before `pay` may force an unwanted draw and additional borrower principal/interest. |
| M-11 | 27–28 | candidate | Permissionless short-interval accrual appears to discard fractional time and underpay LP interest and fee bases. |
| M-12 | 28–29 | candidate | Checking the receiver's rather than controller's `maxWithdraw` may permit withdrawal beyond the controller's actual claimable limit. |

## Low, informational, and gas

| Report ID | Pages | Preliminary status | PDF-grounded reason |
|---|---:|---|---|
| L-1 | 30 | exclude | Upgrade-safe storage layout is a hardening recommendation without a demonstrated collision in the audited snapshot. |
| L-2 | 30–31 | exclude | Zero-address controller state is described as validation/state hygiene; no concrete asset-loss path is shown. |
| L-3 | 31 | hold | The invariant describes possible extraction of reserved assets, but the report notes the current FixedTerm state machine may make it unreachable. |
| L-4 | 31–32 | exclude | EIP-712 is recommended hardening; the PDF does not demonstrate a concrete replay or signature exploit. |
| L-5 | 32 | exclude | Unencrypted deployment-key handling is operational script hygiene and outside the audited runtime-contract detect scope. |
| I-1 | 33 | exclude | Accidental admin/owner renouncement is privileged operational hardening. |
| I-2 | 33 | exclude | `Ownable2Step` is a best-practice recommendation. |
| I-3 | 33 | exclude | Minimum-deposit enforcement is a design recommendation. |
| I-4 | 33 | exclude | ERC-7540 conformance differences are acknowledged and do not establish asset loss. |
| I-5 | 34 | exclude | Incorrect event metadata does not change balances or authorization. |
| I-6 | 34–35 | exclude | Zero-value ERC-20 transfer behavior is standards compatibility, not asset loss. |
| I-7 | 35 | exclude | Modifier ordering is stylistic absent a demonstrated state-changing exploit. |
| I-8 | 35–36 | exclude | Unused error declarations do not affect execution. |
| I-9 | 36 | exclude | Missing events affect observability but not state-transition authorization or balances. |
| G-1 | 37 | exclude | Storage-read optimizations are gas-only. |

## Required code-grounding questions

For every `candidate` or `hold` row, record:

```text
report_finding_id
full PDF title
reported severity
selected exported pages
affected audited files
contracts and functions
attacker prerequisites
root cause
exploit or failure sequence
direct or indirect asset-loss path
vulnerable code lines
reachable test or static proof
fix commit used only as corroboration
distinctness decision
final disposition and reason
```

Every `exclude` row must also receive a code-grounded reason. A preliminary
PDF-only exclusion is not final.

## Mandatory merge/split review

The following clusters share mechanisms, outcomes, or fix commits and must not
be assigned independent EVMBench scores until exact-code review:

1. `C-1`, `C-2`, `C-3`: cancellation/queue advancement and permanent queue
   blockage.
2. `C-4`, `H-1`, `M-09`: `ProcessingMode.RequestPrice`; all are reported as
   resolved by removal or changes around the same pricing mode, including fix
   commit `4e5eef57464d548ec09048eae27b6fcc1489a5c3`.
3. `H-2`, `M-07`: open-term debt/interest/fee accounting; both cite
   `fce6961c71269739ec35da60131eaf63e66e1726` and
   `8e53eba7340f223f86c9c392f50b8b2d885fdd39`.
4. `M-05`, `L-3`: reservation creation versus strategy consumption of reserved
   liquidity.

Use both tests:

```text
Would the same minimal vulnerable-code change remove both issues?
Would the grader be able to distinguish the two root causes from an agent report?
```

If either answer is unclear, hold the scoring split for human review.

## Count reconciliation

| Severity | PDF count | Worksheet count |
|---|---:|---:|
| Critical | 4 | 4 |
| High | 2 | 2 |
| Medium | 12 | 12 |
| Low | 5 | 5 |
| Informational | 9 | 9 |
| Gas | 1 | 1 |
| Total | 33 | 33 |

No final selected-finding count, EVMBench `H-*` mapping, awards, or grader
`max_score` exists yet.
