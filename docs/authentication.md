# 🔑 Authentication & Session Management

RubiFlow offers multiple flexible ways to authenticate and manage user sessions.

---

## 1. Automatic Firefox Session Import (`Client.from_firefox()`)

If you have already logged in to `m.rubika.ir` or `web.rubika.ir` using Firefox on your desktop, RubiFlow can automatically detect and decrypt your active session directly from the Firefox profile storage.

```python
from rubiflow import Client

async with Client.from_firefox() as app:
    me = await app.get_me()
    print("Welcome,", me.full_name)
```

> **Note:** Supported on both native Linux/macOS Firefox and Ubuntu Snap Firefox installations.

---

## 2. Portable StringSessions (`app.session.to_string()`)

StringSessions are compact, self-contained base64 strings containing the auth token, RSA private key, and DC endpoint. They allow you to deploy bots on cloud platforms (Docker, VPS, Heroku) without needing persistent files.

### Exporting a StringSession
```python
import asyncio
from rubiflow import Client

async def export():
    async with Client.from_firefox() as app:
        session_token = app.session.to_string()
        print("Your StringSession:\n", session_token)

asyncio.run(export())
```
The output format looks like:
```text
RubiFlow$eyJhdXRoIjoiZndnbmlkb2p0bnFkZGNycXVl...
```

### Loading a StringSession
```python
import os
from rubiflow import Client

session_token = os.environ.get("RUBIFLOW_SESSION")
app = Client(session=session_token)

async def main():
    async with app:
        me = await app.get_me()
        print("Running as:", me.username)
```

---

## 3. Local File Sessions

You can save and load sessions using JSON files:

```python
# Save to file
app.session.save_to_file("account.session")

# Load from file
app = Client(session="account.session")
```

---

## 4. Manual Login with Phone Number (Programmatic)

For headless logins using SMS or in-app code verification:

```python
import asyncio
from rubiflow import Client

async def login():
    app = Client() # Generates temporary RSA keys and session
    phone = "09123456789"

    # 1. Send SMS code
    res = await app.send_code(phone)
    phone_code_hash = res["data"]["phone_code_hash"]

    # 2. Input code
    code = input("Enter verification code: ")

    # 3. Complete sign-in
    sign_res = await app.sign_in(phone, phone_code_hash, code)
    print("Logged in successfully! Token:", app.session.to_string())

asyncio.run(login())
```
