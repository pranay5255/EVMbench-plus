# [H-01] Unguarded Safe control lets owners erase and bypass accrued fees

## Affected code

- contracts/auth/AdminVault.sol: setFeeTimestamp
- contracts/auth/FeeTakeSafeModule.sol: takeFees
- contracts/SequenceExecutor.sol: executeSequence and _executeAction

## Root cause

The protocol assumes that a user's Safe will interact only through the approved
SequenceExecutor flow and will keep the fee-taking module enabled, but the
audited snapshot installs no Safe transaction guard that enforces either
assumption.

AdminVault.setFeeTimestamp is intentionally keyed by msg.sender and has no
caller restriction. An owner-controlled Safe can therefore call it directly
for any registered pool and replace the Safe's accrued-fee timestamp with the
current block time. The same unrestricted Safe control lets the owner disable
FeeTakeSafeModule or make direct calls outside the approved action flow.

These are manifestations of one missing boundary: the user-controlled Safe is
also trusted to preserve the protocol's fee-enforcement path.

## Prerequisites

- A user controls a Brava Safe with a registered pool position.
- Time has elapsed since the position's last fee timestamp.
- The Safe is not protected by a guard that restricts state-changing calls to
  SequenceExecutor.

## Exploit sequence

1. The user accumulates fees while holding a position in the Safe.
2. Before withdrawing, the user makes the Safe call
   AdminVault.setFeeTimestamp for that position's registered pool.
3. AdminVault stores block.timestamp under the Safe's own fee record.
4. The user executes the normal withdrawal action.
5. ActionBase calculates fees only for the negligible interval since the
   attacker-controlled reset, instead of for the full holding period.

The owner can also disable the fee module and use unrestricted Safe calls as
additional ways to stay outside the intended collection path.

## Impact

The user keeps assets that should have been transferred to the configured fee
recipient. The loss scales with the position balance, configured annual fee,
and elapsed time, and can be repeated for every registered position owned by
the Safe.

## Code evidence

AdminVault accepts a timestamp reset from any caller and keys the write to that
caller:

    function setFeeTimestamp(string calldata _protocolName, address _pool) external {
        _isPool(_pool);
        uint256 protocolId = _protocolIdFromName(_protocolName);
        lastFeeTimestamp[msg.sender][protocolId][_pool] = block.timestamp;
    }

ActionBase later trusts the stored timestamp when calculating the amount to
transfer:

    uint256 lastFeeTimestamp =
        ADMIN_VAULT.getLastFeeTimestamp(protocolName(), _pool);
    uint256 fee =
        _calculateFee(balance, _feePercentage, lastFeeTimestamp, block.timestamp);
    vault.safeTransfer(ADMIN_VAULT.feeConfig().recipient, fee);

The vulnerable tree contains no guard that restricts Safe transactions to the
SequenceExecutor.

## Remediation

Install and enforce a Safe transaction and module guard that permits
state-changing user transactions only through the approved SequenceExecutor
path. Treat fee timestamp changes as protocol-controlled state and test direct
Safe calls, module removal, arbitrary call, and arbitrary delegatecall
attempts.

# [H-02] Unrestricted exit entry points withdraw positions without charging fees

## Affected code

- contracts/SequenceExecutor.sol: _executeAction
- contracts/actions/common/AaveWithdraw.sol: exit
- contracts/actions/common/CompoundV2Withdraw.sol: exit
- contracts/actions/common/ERC4626Withdraw.sol: exit
- contracts/actions/clearpool/ClearpoolWithdraw.sol: exit

## Root cause

Several approved withdrawal action contracts expose external emergency exit
functions that redeem an entire position without calling ActionBase._processFee.
SequenceExecutor selects a whitelisted action address but blindly
delegatecalls user-supplied calldata; it does not require the
executeAction(bytes,uint16) selector. A Safe owner can therefore reach each
exit function through the otherwise approved SequenceExecutor path.

This is distinct from the missing Safe guard: even a guard that restricts the
Safe to SequenceExecutor still permits these selector-level bypasses.

## Prerequisites

- The Safe holds Aave, Compound-style, ERC-4626, or Clearpool position tokens.
- The corresponding withdrawal action is registered in AdminVault.
- Fees have accrued since the last fee timestamp.

## Exploit sequence

1. The user supplies a registered withdrawal action ID to SequenceExecutor.
2. Instead of encoding executeAction, the user encodes that action's exit
   selector and the relevant pool or receipt-token address.
3. SequenceExecutor delegatecalls the action in the Safe's storage and asset
   context.
4. exit redeems the complete position directly from the underlying protocol.
5. Because exit never calls _processFee, no position tokens are transferred to
   Brava's fee recipient.

## Impact

The user receives the underlying assets while retaining all accrued
asset-denominated fees. Brava permanently loses the fee amount for each
position exited through this path.

## Code evidence

SequenceExecutor forwards arbitrary calldata to the selected action:

    address actionAddr =
        ADMIN_VAULT.getActionAddress(_currSequence.actionIds[_index]);
    delegateCall(actionAddr, _currSequence.callData[_index]);

The generic ERC-4626 emergency path performs no fee processing:

    function exit(address _vault) external virtual {
        uint256 maxWithdrawAmount = _getMaxWithdraw(_vault);
        _executeWithdraw(_vault, maxWithdrawAmount);
    }

Equivalent fee-free exit functions exist for the Aave, Compound V2, and
Clearpool withdrawal implementations.

## Remediation

Remove the stale exit entry points or route every reachable redemption path
through the same fee-settlement invariant as executeAction. Restrict
SequenceExecutor to the intended action selector and add tests proving that
alternate external selectors cannot bypass _processFee.

# [H-03] SendToken exports fee-bearing position tokens before fees are settled

## Affected code

- contracts/actions/utils/SendToken.sol: executeAction and _sendToken
- contracts/actions/ActionBase.sol: _processFee

## Root cause

SendToken is an approved generic transfer action. It verifies only that the
recipient is an owner of the Safe and then transfers any requested ERC-20 token.
It neither identifies registered pool or receipt tokens nor checks or updates
their fee timestamp, and it never calls _processFee.

Receipt tokens are the balances from which Brava charges annual fees. Once a
user transfers those tokens out of the Safe, the user can redeem them directly
at the underlying protocol while Brava's accounting remains in the abandoned
Safe.

## Prerequisites

- The Safe holds a transferable tokenized position, such as an Aave aToken.
- SendToken is registered as an approved action.
- Fees have accrued on the position.

## Exploit sequence

1. The user executes SendToken through SequenceExecutor.
2. The user selects the fee-bearing position token and their own address as the
   recipient.
3. SendToken transfers the entire receipt-token balance without settling the
   position's accrued fees.
4. The user redeems the position tokens directly through the underlying
   protocol.
5. The Safe no longer holds the fee-bearing balance from which Brava could
   collect the skipped amount.

## Impact

The user exits with the full position value and avoids the asset-denominated
fee owed to Brava. The configured fee recipient loses the accrued amount.

## Code evidence

SendToken checks the recipient but performs no fee synchronization:

    require(
        ownerManager.isOwner(inputData.to),
        Errors.Action_InvalidRecipient(protocolName(), actionType())
    );
    _sendToken(inputData.tokenAddr, inputData.to, inputData.amount);

The transfer helper sends the selected token directly:

    if (_amount == type(uint256).max) {
        _amount = IERC20(_tokenAddr).balanceOf(address(this));
    }
    IERC20(_tokenAddr).safeTransfer(_to, _amount);

No call to AdminVault.getLastFeeTimestamp, setFeeTimestamp, or _processFee
occurs on this path.

## Remediation

Before transferring a registered fee-bearing token, settle its accrued fee and
update the timestamp, or reject such tokens from the generic transfer action.
Keep the check tied to the token address so receipt tokens cannot bypass it
through a different protocol label.
