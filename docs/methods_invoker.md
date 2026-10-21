# ⚡ Direct RPC Invoker (`app.invoke`)

While RubiFlow provides high-level typed helper methods for common operations, it also provides a direct low-level invoker capable of executing **any of the 301 reverse-engineered RPC methods** with arbitrary payloads.

---

### Syntax

```python
result = await app.invoke(method_name: str, **kwargs)
```

The invoker automatically:
1. Wraps your arguments into the required Rubika RPC envelope.
2. Resolves the correct API endpoint (Messenger, Rubino, or VOD).
3. Generates the 32-character AES key and encrypts the payload using AES-256-CBC.
4. Encodes and disguises the authentication token using the `em` substitution cipher.
5. Signs the request using RSA-SHA256 (if temporary key is active).
6. Decrypts and unpacks the JSON response from the server.

---

### Example: Invoking any Raw Method

```python
from rubiflow import Client

app = Client.from_firefox()

async def main():
    async with app:
        # Call raw 'getUserInfo'
        user_raw = await app.invoke("getUserInfo", user_guid="u0ABCDEF...")
        print(user_raw)

        # Call raw Rubino method
        explore_raw = await app.invoke("getExplorePosts", limit=10)
        print(explore_raw)

if __name__ == "__main__":
    app.run(main())
```

---

### Full Catalog of 301 Supported Methods

Refer to the complete reverse-engineered catalog:
- 👉 [All 301 Methods Catalog](RUBIKA_API_FULL_REFERENCE.md)
