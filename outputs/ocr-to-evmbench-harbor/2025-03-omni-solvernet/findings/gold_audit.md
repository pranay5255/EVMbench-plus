# Omni SolverNet detect findings

This audit package contains four distinct loss-of-assets root causes from the
Sigma Prime Omni SolverNet report. Findings are ordered by report ID and do not
include availability-only or informational observations.

## H-01

Reentrant fill acknowledgement lets a filled owner reclaim the source deposit.
See `findings/H-01.md`.

## H-02

Underestimated fill gas makes a cross-chain fill acknowledgement fail. See
`findings/H-02.md`.

## H-03

Fixed close buffer allows filled orders to reclaim deposits during portal
downtime. See `findings/H-03.md`.

## H-04

Reentrant middleman callbacks steal in-flight token or native balances. See
`findings/H-04.md`.
