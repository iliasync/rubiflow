# ⚠️ Errors & Exception Handling

RubiFlow provides a clear, structured exception hierarchy to help you handle network failures, authentication revocations, and server-side RPC errors gracefully.

---

## Exception Hierarchy

```
Exception
 └── RubiFlowError (Base exception for all library errors)
      ├── ApiError (Raised when Rubika RPC returns non-OK status)
      │    ├── InvalidAuthError (Session token is invalid, revoked, or expired)
      │    ├── RateLimitError (Too many requests in a short time window)
      │    └── AccessDeniedError (Insufficient permissions or blocked)
      ├── NetworkError (HTTP connection errors, DNS failure)
      │    └── TimeoutError (Request timed out waiting for server response)
      └── CryptoError (AES/RSA encryption, decryption, or padding failure)
```

---

## The `ApiError` Class

When Rubika's server responds with an error status (e.g., `ERROR_GENERIC`, `INVALID_AUTH`), RubiFlow raises an `ApiError` with detailed diagnostic attributes:

### Attributes
| Attribute | Type | Description |
| :--- | :--- | :--- |
| `code` | `str` | Top-level status code (e.g. `'ERROR_GENERIC'`, `'ERROR_ACTION'`). |
| `status_det` | `str` | Detailed error descriptor from Rubika (e.g. `'INVALID_AUTH'`, `'NOT_REGISTERED'`). |
| `status_code` | `int` | HTTP response code (usually `200` because Rubika returns RPC errors in JSON). |
| `message` | `str` | Human-readable explanation. |

---

## Common Rubika RPC Error Codes

| Error Code | Status Detail (`status_det`) | Cause & Resolution |
| :--- | :--- | :--- |
| `ERROR_GENERIC` | `INVALID_AUTH` | The auth token has expired or been terminated by user. RubiFlow raises `InvalidAuthError`. Call `interactive_login()` to re-authenticate. |
| `ERROR_GENERIC` | `TOO_MANY_REQUESTS` | You have exceeded rate limits. Add exponential backoff (`asyncio.sleep(3)`). |
| `ERROR_GENERIC` | `ACCESS_DENIED` | Account lacks permission (e.g. attempting to pin message in a group without admin rights). |
| `ERROR_ACTION` | `NOT_REGISTERED` | The provided phone number is not registered on Rubika. |
| `ERROR_GENERIC` | `CHAT_NOT_FOUND` | Target GUID does not exist or user has not joined the group/channel. |
| `ERROR_GENERIC` | `MESSAGE_NOT_FOUND` | Target message ID was deleted or invalid. |
| `ERROR_GENERIC` | `INVALID_INPUT` | Malformed parameters or missing required fields in RPC payload. |

---

## Recommended Error Handling Patterns

### 1. Handling Authentication Expiry
```python
from rubiflow import Client
from rubiflow.exceptions import InvalidAuthError, ApiError

app = Client("bot")

async def safe_execute():
    try:
        async with app:
            await app.send_message("u0...", "Hello!")
    except InvalidAuthError:
        print("[!] Session revoked. Re-authenticating...")
        await app.interactive_login()
    except ApiError as exc:
        print(f"[!] Server RPC Error: {exc.code} - {exc.status_det}")
```

### 2. Handling Rate Limits with Retry Backoff
```python
import asyncio
from rubiflow.exceptions import ApiError

async def send_with_retry(app, target, text, max_retries=3):
    delay = 2
    for attempt in range(max_retries):
        try:
            return await app.send_message(target, text)
        except ApiError as exc:
            if exc.status_det == "TOO_MANY_REQUESTS":
                print(f"[!] Rate limited. Sleeping for {delay} seconds...")
                await asyncio.sleep(delay)
                delay *= 2
            else:
                raise
```
