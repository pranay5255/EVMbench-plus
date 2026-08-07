# P4 finding grounding — H-01 / L-7

## Report evidence

- PDF pages 23–24, finding **L-7**
  “Rounding Error Allows Theft of User Deposits via Donation Attack”
- Status Fixed; client fix commit `9f5f362a3723e9ec6fe8686fd30a22948653e1d8`
- OCR slices: `ocr_evidence/pdf_003345_a305f8485f3a/H-01.pages.jsonl` (pages 23–24, byte-exact)

## Code at vulnerable commit `57d820afa1d58bf89073e668f5608942d90188c7`

```text
contracts/AlgebraVault.sol:42  uint256 constant MIN_SHARES = 1000;
contracts/AlgebraVault.sol:~581-588
  shares = shares.mul(_totalSupply).div(pool0PricedInToken1.add(pool1));
  // no shares==0 check
  _mint(to, shares);
```

## Fix commit (not the task snapshot)

`9f5f362a3723e9ec6fe8686fd30a22948653e1d8`:

- `MIN_SHARES = 1e6`
- `if (shares == 0) revert InvalidDeposit();`

Confirmed ancestor of re-audit commit `d637339f968d67f175e8cb56ce3ae54a69bdefee`.

## Asset-loss path

Attacker first-deposits dust → donates tokens → victim deposit rounds to 0
shares → attacker withdraws all shares including victim tokens. Direct loss of
user deposit assets.
