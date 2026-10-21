# 💳 Wallet & Payments API

Methods for querying in-app balance, checking transaction logs, and transferring credit between users.

---

### `get_wallet_status`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Returns the user's current digital wallet balance and currency codes.

```python
status = await app.get_wallet_status()
print(f"Available Balance: {status.get('balance')} Rials")
```

---

### `get_wallet_transactions`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Fetches recent transaction history with timestamps, amounts, and statuses.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `limit` | `int` | No | Number of transactions (default `20`). |

---

### `transfer_credit`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Transfers balance directly to another Rubika user.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `recipient_guid` | `str` | Yes | Target user GUID (`u...`). |
| `amount` | `int` | Yes | Amount in Rials. |
