# P2 PDF/OCR side-by-side review: Securitize

| Page | Role | Notes |
|---:|---|---|
| 1 | identity | Cyfrin Securitize On-Off Ramp and Bridge v2.1, 2025-07-23 |
| 2–3 | summary/TOC | Finding list and page map |
| 4–5 | protocol | Product summary; not gold |
| 6–7 | scope | Contract path list for on-off + bridge; report uses `bc-on-off-contracts\` / `bridge-contracts\` prefixes |
| 8 | scope/summary | Table: `bc-on-off-ramp-sc` commit `a944bb11b106…`, fix `4a426e689586…`; bridge `bc-securitize-bridge-sc` `60b6ef00e8a8…` / fix `1da35cde31a5…` |
| 9 | summary | Finding status table |
| 10–11 | finding C-1 | Nonce replay critical; selected |
| 12 | M-1 / start M-2 | M-1 excluded; M-2 bridge held |
| 13–14 | M-2/M-3/start M-4 | Bridge held; M-4 continue |
| 14–15 | M-4 end | Excluded under loss_of_assets |
| 15–22 | lows | Mostly exclude / bridge-held |
| 22–27 | informational | Exclude |

## Corrections applied only in gold text

- Path prefix mapped to repository `contracts/` layout.
- Full vulnerable commit expanded via GitHub object for prefix `a944bb11b106` →
  `a944bb11b106c13a5e43f8de01c9c01eeb5bb472` (unique match).
- Repository URL recovered from PDF hyperlinks on fix commits:
  `https://github.com/securitize-io/bc-on-off-ramp-sc`.
- Bridge host recovered as Bitbucket `securitize_dev/bc-securitize-bridge-sc`
  (private/unavailable).

Immutable OCR JSONL was not rewritten.
