# ⚡ Direct RPC Invoker (`app.invoke` & `app.execute`)

While RubiFlow provides high-level typed helper methods for common operations, it also provides a direct, low-level invoker capable of executing **any of the 301 reverse-engineered RPC methods** with arbitrary payloads.

This guarantees that even if Rubika introduces brand-new RPC methods or experimental endpoints tomorrow, your application can invoke them immediately without waiting for a library update.

---

## 1. High-Level Invoker: `app.invoke`

The `invoke` method accepts the RPC method name and key-value arguments, automatically serializing them into Rubika's protocol envelope.

### Syntax
```python
result = await app.invoke(method: str, **kwargs) -> Dict[str, Any]
```

### Automatic Pipeline
When you call `app.invoke("sendMessage", object_guid="u0...", text="Hello")`, RubiFlow automatically:
1. Wraps arguments into the standard `{ "method": ..., "input": {...}, "client": {...} }` RPC envelope.
2. Derives the 32-character AES secret key from the current session auth token.
3. Pads and encrypts the inner JSON payload using **AES-256-CBC with zero IV**.
4. Generates an **RSA-SHA256 signature** over the encrypted payload using the session's private key.
5. Disguises the auth token with the proprietary **`em` character substitution cipher**.
6. Sends the payload via HTTP POST through the high-performance `aiohttp` connection pool.
7. Decrypts and unpacks the returned `data_enc` payload into a native Python dictionary.
8. Checks the response status code and raises appropriate typed exceptions on errors.

---

## 2. Low-Level Invoker: `app.execute`

For fine-grained control over the input dictionary and API versions (e.g. V6, V4, V0), use `app.execute`:

### Syntax
```python
result = await app.execute(
    method: str,
    input_data: Optional[Dict[str, Any]] = None,
    api_version: str = "6"
) -> Dict[str, Any]
```

### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `method` | `str` | Yes | - | Name of the RPC method (case-sensitive, e.g. `'getUserInfo'`). |
| `input_data` | `Dict[str, Any]` | No | `{}` | Dictionary of input parameters for the method. |
| `api_version` | `str` | No | `'6'` | Protocol API version (`'6'` for standard, `'4'` for DCs, `'0'` for base info). |

---

## 3. Practical Invoker Examples

### Example 1: Calling Base Platform Info (V0 API)
```python
from rubiflow import Client

async def get_system_info():
    async with Client() as app:
        # Calls getBaseInfo on API version 0
        base_info = await app.execute("getBaseInfo", {}, api_version="0")
        print("Server Timestamp:", base_info.get("data", {}).get("server_time"))
```

### Example 2: Calling Data Center URLs (V4 API)
```python
async def get_active_dcs():
    async with Client() as app:
        dcs_response = await app.execute("getDCs", {}, api_version="4")
        print("Active Data Centers:", dcs_response.get("data", {}).get("dcs"))
```

### Example 3: Calling Rubino Explore Feed with Raw Pagination
```python
async def explore_raw():
    async with Client() as app:
        res = await app.invoke("getExplorePosts", limit=50, sort="trend")
        for post in res.get("data", {}).get("posts", []):
            print(f"Post ID: {post['id']} by @{post['profile']['username']}")
```

### Example 4: Calling Experimental or Custom RPC Methods
```python
async def custom_method():
    async with Client() as app:
        result = await app.invoke(
            "requestDeleteAccount",
            reason="Testing account lifecycle"
        )
        print("Result:", result)
```

---

## 4. Complete Catalog of 301 Methods

To look up any method name and its required input arguments:
- 👉 [All 301 Methods Catalog](RUBIKA_API_FULL_REFERENCE.md)
