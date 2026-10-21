# 💳 Wallet & Payments API

Methods for querying digital wallet balance, transaction logs, currency exchange info, and transferring credit.

---

### `get_wallet_status`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Returns the user's current digital wallet balance and currency codes.

#### Return Value
```json
{
  "status": "OK",
  "data": {
    "balance": 500000,
    "currency": "IRR",
    "is_active": true,
    "wallet_id": "w0ABCDEF12345"
  }
}
```

#### Code Example
```python
wallet = await app.get_wallet_status()
print(f"Balance: {wallet['data']['balance']:,} Rials")
```

---

### `get_wallet_transactions`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Retrieves the recent history of deposits, withdrawals, and payments.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | No | `20` | Number of recent transactions to return. |

#### Code Example
```python
txs = await app.get_wallet_transactions(limit=10)
for tx in txs:
    print(f"[{tx['date']}] {tx['type']}: {tx['amount']} Rials - Status: {tx['status']}")
```

---

### `transfer_credit`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Transfers in-app balance directly to another Rubika user.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `recipient_guid` | `str` | Yes | - | Target user GUID (`u0...`). |
| `amount` | `int` | Yes | - | Amount in Rials. |

---

### `get_wallet_currencies`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Returns supported currencies and digital token definitions.
