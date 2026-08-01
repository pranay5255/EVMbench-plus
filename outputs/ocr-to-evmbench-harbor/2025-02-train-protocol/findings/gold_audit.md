# [H-01] Uniform minimum timelocks let an LP refund and then redeem

## Affected code

- `chains/evm/solidity/contracts/HashedTimeLockERC20.sol`:
  `_validTimelock`, `lock`, and `addLock`
- `chains/evm/solidity/contracts/HashedTimeLockEther.sol`:
  `_validTimelock`, `lock`, and `addLock`

## Root cause

Both the user's source-chain commitment and the LP's destination-chain lock
only have to expire 15 minutes after the transaction that creates or updates
them. The contracts enforce no ordering or safety gap between the two sides of
the atomic swap.

The LP creates its destination lock first. The user can only finalize the
source commitment with `addLock` afterward, so even when both parties choose
the minimum duration, the user's source timelock expires later than the LP's
destination timelock.

## Prerequisites

- The LP chooses the minimum allowed destination-chain timelock.
- The client accepts the LP lock without requiring a sufficient cross-chain
  timelock gap.
- The user finalizes the source-chain commitment after the LP transaction.

## Exploit sequence

1. The user commits source-chain funds for the LP.
2. The LP creates the destination lock with an expiry at `T + 900`.
3. The user later calls `addLock`; its minimum expiry is necessarily later
   than the LP's because it is validated against a later block timestamp.
4. When the destination lock expires, the LP refunds its own funds.
5. The user's source lock is still active, so the LP uses the revealed secret
   to redeem the user's committed funds.

## Impact

The LP recovers its destination-chain assets and also takes the user's
source-chain assets. The user cannot refund while the later source timelock is
still active.

## Code evidence

Both Solidity implementations apply the same independent minimum:

```solidity
modifier _validTimelock(uint48 timelock) {
    if (block.timestamp + 900 > timelock) revert InvalidTimelock();
    _;
}
```

`addLock` then overwrites the source commitment's timelock without relating it
to the destination lock:

```solidity
htlc.hashlock = hashlock;
htlc.timelock = timelock;
```

## Remediation

Enforce the protocol's cross-chain timelock ordering in the contracts or in a
mandatory validated quote. The destination lock must retain a sufficient
safety window beyond the source-side refund/redeem sequence; two independent
15-minute minima are not enough.

# [H-02] Nominal fee-on-transfer accounting spends other users' deposits

## Affected code

- `chains/evm/solidity/contracts/HashedTimeLockERC20.sol`: `commit`, `lock`,
  `redeem`, and `refund`

## Root cause

`commit` and `lock` transfer an ERC-20 amount and then record the caller's
nominal `amount` in the HTLC. They never measure the contract's balance change.
For a fee-on-transfer token, the contract receives less than the recorded
principal while promising the full nominal principal to the redeemer or
refunder.

## Prerequisites

- The token charges a transfer fee or otherwise delivers less than the
  requested transfer amount.
- The contract already holds the same token for other HTLCs, or a later user
  deposits it.

## Failure sequence

1. A user requests a lock for `amount + reward`.
2. `safeTransferFrom` succeeds, but the token credits the contract with less
   than that amount.
3. The HTLC records the full nominal `amount`, and the reward mapping records
   the nominal reward.
4. A redeem or refund pays the recorded value.
5. If enough pooled balance exists, the payout consumes tokens belonging to
   other HTLCs. Otherwise, the payout reverts and the underfunded user cannot
   recover the recorded amount.

## Impact

An early redeemer or refunder can spend other users' deposits, leaving later
HTLCs insolvent. With insufficient pooled liquidity, users' redemptions and
refunds remain blocked because the contract promises more tokens than it
received.

## Code evidence

The transfer uses the nominal amount:

```solidity
token.safeTransferFrom(msg.sender, address(this), amount + reward);
```

The HTLC then records that nominal principal without checking the received
balance:

```solidity
contracts[Id] = HTLC(
    amount,
    hashlock,
    uint256(1),
    tokenContract,
    timelock,
    uint8(1),
    payable(msg.sender),
    payable(srcReceiver)
);
```

Later paths pay `htlc.amount` and `rewards[Id].amount` from the contract's
shared token balance.

## Remediation

Either reject tokens whose post-transfer balance delta differs from the
requested value, or record and emit the exact received amount while applying
the same rule to rewards. Never promise a nominal amount that the contract did
not receive.

# [H-03] Unchecked Starknet token returns finalize unfunded HTLCs

## Affected code

- `chains/starknet/src/HashTimeLockedERC20.cairo`: `commit`, `lock`, `redeem`,
  and `refund`

## Root cause

The Cairo contract calls ERC-20 `transfer_from` and `transfer` but ignores
their boolean return values. A standards-compatible token may return `false`
instead of reverting. The contract then continues to write HTLC state, emit
cross-chain events, or mark a claim complete even though no assets moved.

## Prerequisites

- The selected Starknet token reports a failed transfer by returning `false`.
- A solver or counterparty trusts the emitted HTLC event or finalized state.

## Failure sequence

1. `commit` or `lock` calls `transfer_from`.
2. The token returns `false`; no tokens enter the contract.
3. Because the return value is ignored, the contract writes an apparently
   funded HTLC and emits its event.
4. A solver observes the event and locks real assets on the destination chain.
5. The initiating user can receive those destination assets even though the
   corresponding Starknet transfer never happened.

The outbound paths have the symmetric failure: `redeem` and `refund` set
`claimed` before calling `transfer`. A `false` return leaves the HTLC finalized
without paying the recipient or refunding the sender.

## Impact

Solvers can lose destination-chain funds to unfunded source-chain HTLCs.
Users can also lose access to deposited tokens when a redeem or refund is
marked complete despite a failed outbound transfer.

## Code evidence

The source deposit return value is discarded:

```cairo
token.transfer_from(get_caller_address(), get_contract_address(), amount);

self.contracts.write(
    Id,
    HTLC {
        amount: amount,
        // ...
    }
);
```

Outbound paths update state before unchecked calls:

```cairo
self.contracts.entry(Id).claimed.write(3);
IERC20Dispatcher { contract_address: htlc.tokenContract }
    .transfer(htlc.srcReceiver, htlc.amount);
```

## Remediation

Require every `transfer_from` and `transfer` result to be `true`, and revert
otherwise so all storage and event changes roll back atomically.

# [H-04] Cached EIP-712 domains permit post-fork signature replay

## Affected code

- `chains/evm/solidity/contracts/HashedTimeLockERC20.sol`: constructor,
  `addLockSig`, and `verifyMessage`
- `chains/evm/solidity/contracts/HashedTimeLockEther.sol`: constructor,
  `addLockSig`, and `verifyMessage`

## Root cause

Each contract computes `DOMAIN_SEPARATOR` once in the constructor and stores it
as an immutable value. The separator includes the deployment-time
`block.chainid`, but `verifyMessage` never recomputes it if the live chain ID
changes after a hard fork.

## Prerequisites

- A chain forks and one branch adopts a different chain ID.
- The HTLC state and contract address exist on both branches.
- An attacker has a valid pre-fork or other-branch `addLockMsg` signature.

## Exploit sequence

1. The HTLC sender signs an `addLockMsg` for one chain context.
2. A hard fork changes `block.chainid` on another live branch.
3. The cached separator still contains the old chain ID.
4. The attacker submits the same signature to `addLockSig` on the unintended
   branch.
5. The contract accepts it and installs the signed hashlock and timelock.
6. The corresponding secret can then redeem forked HTLC assets that the sender
   did not intend to authorize on that branch.

## Impact

Signatures intended for one fork can authorize lock changes on another,
exposing the sender's forked HTLC assets to replay and redemption.

## Code evidence

The domain is cached only at deployment:

```solidity
constructor() {
    DOMAIN_SEPARATOR = hashDomain(
        EIP712Domain({
            name: "LayerswapV8",
            version: "1",
            chainId: block.chainid,
            verifyingContract: address(this),
            salt: 0x2e4ff7169d640efc0d28f2e302a56f1cf54aff7e127eededda94b3df0946f5c0
        })
    );
}
```

Every later verification uses that immutable value:

```solidity
bytes32 digest =
    keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, hashMessage(message)));
return ECDSA.recover(digest, v, r, s) == contracts[message.Id].sender;
```

## Remediation

Use an EIP-712 implementation that caches both the deployment chain ID and
separator, then rebuilds the separator from the current `block.chainid` when
they differ.
