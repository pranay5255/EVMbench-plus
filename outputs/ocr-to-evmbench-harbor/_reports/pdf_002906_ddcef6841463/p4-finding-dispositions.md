# UFarm finding dispositions before code grounding

No finding is selected. The PDF-level assessment below prevents the repository
failure from hiding potentially relevant findings, but none may become gold
until the exact audited commit is checked out and each mechanism is verified in
that tree.

| Report ID | Pages | Severity | PDF-level asset-loss assessment | Disposition |
|---|---:|---|---|---|
| UFARM1-2 | 9–11 | Critical | Permissionless queue congestion allegedly makes the oracle callback permanently uncallable, potentially freezing pool deposits and withdrawals. | Hold: potentially indirect asset lock, but exact vulnerable code and recovery behavior are unavailable. |
| UFARM1-1 | 12–14 | High | A privileged top-up approver can allegedly replay signed requests, pulling extra user tokens or shares beyond the intended request. | Hold: concrete direct asset-loss candidate, but ungrounded in audited code. |
| UFARM1-4 | 15–16 | High | A zero-output withdrawal can allegedly let a user force pool deactivation. | Exclude provisionally: availability/state-transition impact only; code still unavailable. |
| UFARM1-9 | 17–20 | High | A nonzero withdrawal lock allegedly makes the investor path unreachable and freezes withdrawals until configuration changes. | Hold: concrete asset-freeze candidate, but ungrounded in audited code. |
| UFARM1-3 | 21 | Medium | LIFO queue processing is unfair but the report gives no concrete asset-loss sequence. | Exclude provisionally: fairness only and code unavailable. |
| UFARM1-6 | 22–23 | Medium | Performance fees are allegedly computed on profit before protocol and management costs, overcharging pool investors. | Hold: concrete value-transfer candidate, but ungrounded in audited code. |
| UFARM1-7 | 24–25 | Medium | Missing minimum output permits unfavorable execution after ordinary pool-value movement. | Hold for semantic review: user value loss is described, but no attacker-controlled sequence is established and code is unavailable. |
| UFARM1-8 | 26–27 | Medium | A blacklisted recipient or reverting token hook can allegedly revert a whole callback batch. | Exclude provisionally: batch availability impact without a distinct asset-loss path; code unavailable. |
| UFARM1-10 | 28–29 | Medium | A permissionless CREATE2 factory call can allegedly front-run an application ID and block fund creation. | Exclude provisionally: creation availability only; code unavailable. |
| UFARM1-5 | 30 | Low | An event reports token amounts in the wrong order. | Exclude: telemetry correctness only, with no asset loss. |

Potential distinct loss-of-assets root causes retained for later code review are
UFARM1-1, UFARM1-2, UFARM1-6, and UFARM1-9. UFARM1-7 needs a stricter semantic
decision after code review. These are not selected findings and are not a gold
answer.
