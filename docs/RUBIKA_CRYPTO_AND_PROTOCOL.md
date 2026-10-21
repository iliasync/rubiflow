# Rubika V6 Protocol & Cryptography Specification

This document details the exact protocol, cryptographic algorithms, payload wrapping, and session handling used by Rubika Web (`web.rubika.ir`) and Rubika PWA (`m.rubika.ir`).

---

## 1. High-Level Architecture

Rubika uses a hybrid cryptographic transport:
1. **Symmetric Encryption (AES-256-CBC):** Used to encrypt the JSON RPC payload (`data_enc`).
2. **Key Derivation (`createSecretPassphrase`):** A custom permutation and Caesar shift applied to the 32-character Auth key or temporary session key.
3. **Token Disguise (`em` cipher):** An alphabet and digit shift cipher applied to the `auth` string sent in the root JSON request.
4. **Asymmetric Signature (RSA-SHA256):** The base64-encoded `data_enc` string is signed with the client's RSA private key (1024-bit or 2048-bit) and sent in the `sign` field.

---

## 2. Request Envelope Structure (Version 6)

Every authenticated request sent to a Rubika DC (e.g. `https://messengerg2c*.iranlms.ir/`) has this JSON structure:

```json
{
  "api_version": "6",
  "auth": "<substituted_auth_key>",
  "data_enc": "<base64_aes_ciphertext>",
  "sign": "<base64_rsa_sha256_signature>"
}
```

For unauthenticated calls (e.g., handshake, `sendCode`, `signIn` before session is established):

```json
{
  "api_version": "6",
  "tmp_session": "<32_random_lowercase_letters>",
  "data_enc": "<base64_aes_ciphertext_encrypted_with_tmp_session>",
  "sign": "<base64_rsa_sha256_signature>"
}
```

The decrypted inner payload of `data_enc` is:

```json
{
  "method": "sendMessage",
  "input": {
    "object_guid": "u0...",
    "rnd": 123456789,
    "text": "Hello from rubika-lib"
  },
  "client": {
    "app_name": "Main",
    "app_version": "4.4.34",
    "platform": "Web",
    "package": "web.rubika.ir",
    "lang_code": "fa"
  }
}
```

---

## 3. Cryptographic Implementation Details

### 3.1 Key Derivation (`createSecretPassphrase`)

Given an auth key or `tmp_session` $A$ of length 32:

1. Divide into 4 chunks of 8 characters:
   $$t = A[0:8], \quad i = A[8:16], \quad p_1 = A[16:24], \quad p_2 = A[24:32]$$
2. Rearrange chunks:
   $$N = p_1 + t + p_2 + i = A[16:24] + A[0:8] + A[24:32] + A[8:16]$$
3. Apply character transformation on each character $c$ of $N$:
   - If $c \in ['0' \dots '9']$:
     $$c' = \text{chr}\left(((c - '0' + 5) \bmod 10) + '0'\right)$$
   - If $c \in ['a' \dots 'z']$:
     $$c' = \text{chr}\left(((c - 'a' + 9) \bmod 26) + 'a'\right)$$
   - Otherwise, $c' = c$.

### 3.2 AES Encryption & Decryption
- **Algorithm:** AES-256-CBC (or AES-128 if 16-byte key)
- **Key:** UTF-8 bytes of `createSecretPassphrase(auth)`
- **IV:** 16 null bytes (`0x00 * 16`)
- **Padding:** PKCS#7

### 3.3 Auth Token Substitution Cipher (`em`)
When sending the `auth` string in the root JSON field, Rubika obfuscates it via character substitution:

```python
def disguise_auth(auth_str: str) -> str:
    res = []
    for c in auth_str:
        if '0' <= c <= '9':
            res.append(chr((13 + (ord(c) - ord('0'))) % 10 + ord('0')))
        elif 'A' <= c <= 'Z':
            res.append(chr((29 - (ord(c) - ord('A'))) % 26 + ord('A')))
        elif 'a' <= c <= 'z':
            res.append(chr((32 - (ord(c) - ord('a'))) % 26 + ord('a')))
        else:
            res.append(c)
    return "".join(res)
```

### 3.4 RSA Signature
- The base64 string `data_enc` is signed using RSA PKCS#1 v1.5 with SHA-256.
- The binary signature is base64-encoded and placed in the `"sign"` key.

---

## 4. Firefox LocalStorage Session Structure

From inspecting the active session in `~/.mozilla/firefox/.../storage/default/https+++web.rubika.ir/ls/data.sqlite`:

| Key | Format | Description |
|-----|--------|-------------|
| `key` | Base64-encoded JSON | `{"version": "6", "d": "-----BEGIN RSA PRIVATE KEY-----\n..."}` |
| `auth` | String | Raw 32 or 64 character session auth token |
| `dcs` | JSON | List of DC endpoints, e.g. `{"default_api_urls": ["https://messengerg2c377.iranlms.ir"]}` |
| `profile` | Encrypted JSON | Encrypted current user profile object |
| `chat_state` | JSON | Synchronization state for chat messages (`start_id`, `has_continue`) |
