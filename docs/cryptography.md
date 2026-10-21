# 🔐 Rubika V6 Cryptography & Security

RubiFlow implements the full **Rubika V6 Protocol**, reverse-engineered from the official Web and PWA clients (`web.rubika.ir` and `m.rubika.ir`).

---

## 1. Key Derivation (`create_secret_passphrase`)

Rubika requires an ephemeral 32-character AES secret key derived from the user's permanent authentication token:

```
Passphrase = Token[0:8] + Token[16:24] + Token[8:16] + Token[24:32]
```

### Python Implementation:
```python
def create_secret_passphrase(auth_token: str) -> str:
    if len(auth_token) < 32:
        auth_token = auth_token.ljust(32, "a")
    return (
        auth_token[0:8]
        + auth_token[16:24]
        + auth_token[8:16]
        + auth_token[24:32]
    )
```

---

## 2. AES-256-CBC Payload Encryption

Every RPC request payload is serialized to JSON, padded with standard PKCS#7 padding, and encrypted using AES-256-CBC:
- **Cipher:** `AES-256-CBC`
- **Key:** Derived 32-byte secret passphrase (`utf-8` encoded).
- **IV:** 16 zero bytes (`b'\x00' * 16`).
- **Encoding:** Base64.

---

## 3. Token Disguise (`disguise_auth` / `em` Cipher)

Rubika passes the authentication token in request headers using a custom character substitution table:

| Plain | Disguised | Plain | Disguised |
| :---: | :---: | :---: | :---: |
| `a` | `g` | `0` | `y` |
| `b` | `h` | `1` | `z` |
| `c` | `i` | `2` | `0` |
| `d` | `j` | `3` | `1` |
| `e` | `k` | `4` | `2` |
| `...` | `...` | `9` | `7` |

RubiFlow handles this translation bidirectionally automatically.

---

## 4. Client Handshake Identification

Rubika validates the inner client header inside the encrypted envelope. Non-standard identifiers are rejected by the server with `ERROR_GENERIC`.

RubiFlow uses the exact compliant descriptor:
```json
{
  "app_name": "Main",
  "app_version": "2.5.9",
  "platform": "PWA",
  "package": "m.rubika.ir",
  "lang_code": "fa"
}
```

Device branding (such as `"RubiFlow Framework"`) is registered via the server's dedicated `registerDevice` RPC method without triggering signature checks.
