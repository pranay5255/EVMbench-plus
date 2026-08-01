# Audit findings

## H-01: Silent inactive reward handling permanently consumes validator claims without payment

`ValidatorRewarder` implements `whenActive` by returning normally when
`_active` is false. A paused call therefore reports success even though the
guarded function body did not execute.

The direct asset-loss path is in `ValidatorRewarder.notifyValidClaim`. The
system uses this callback to mint or transfer a validator's checkpoint reward.
When the rewarder is inactive, the callback silently succeeds without issuing
tokens. The outer consensus-claim processor can then consume the claim, leaving
the validator permanently unable to recover that reward.

The modifier must revert when inactive so the outer transaction rolls back and
the claim remains retryable. PR #57 implements that behavior with
`ContractNotActive()`.
