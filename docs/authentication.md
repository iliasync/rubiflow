# 🔑 Authentication & Session Management

RubiFlow provides seamless, Pyrogram/Telethon-style session management with automatic terminal login, custom session file naming, Firefox session auto-import, and portable StringSessions.

---

## 1. Terminal Interactive Login (Recommended)

Like popular Telegram frameworks, you can specify a session name or omit it to use the default session file (`rubiflow.session`).

```python
import asyncio
from rubiflow import Client

async def main():
    # Pass a custom session name or omit for 'rubiflow.session'
    app = Client("my_bot")

    async with app:
        me = await app.get_me()
        print(f"Logged in as: {me.full_name} (@{me.username})")

asyncio.run(main())
```

### How It Works:
1. **Existing Session Found:** If `my_bot.session` exists on disk, RubiFlow loads it instantly and authenticates without prompting.
2. **First-Time Setup (Terminal Prompt):** If the session file does not exist, RubiFlow launches the interactive terminal assistant:
   - **Phone Number:** Prompts for your phone number (`+989...` or `09...`). Automatic normalization handles Iranian and international formats.
   - **Activation Code:** Sends code via SMS or the official Rubika application and prompts for the code.
   - **Two-Step Verification (2FA):** If 2FA is active, prompts for your password with hidden characters (`getpass`).
   - **Device Registration:** Registers device identification as `"RubiFlow Framework"`.
   - **Auto-Save:** Saves the session credentials to `my_bot.session` so you never have to log in again!

---

## 2. Session File Naming Rules

You can name your session files however you like:

| Syntax | Generated File | Description |
| :--- | :--- | :--- |
| `Client()` | `rubiflow.session` | **Default:** Standard default session file. |
| `Client("bot")` | `bot.session` | Automatically adds `.session` extension. |
| `Client("account.json")` | `account.json` | Custom explicit filename and extension. |
| `Client(session_name="work")` | `work.session` | Explicit keyword argument. |
| `Client(":memory:")` | In-Memory | Ephemeral session without disk persistence. |

---

## 3. Automatic Firefox Session Import (`Client.from_firefox()`)

If you are logged into `web.rubika.ir` or `m.rubika.ir` on Firefox, RubiFlow can decrypt and load your session instantly with zero SMS codes:

```python
from rubiflow import Client

# Direct import from Firefox browser
app = Client.from_firefox()

async with app:
    me = await app.get_me()
    print("Welcome,", me.full_name)
```

You can also import from Firefox and save directly to a named session file:
```python
# Imports from Firefox and saves to my_bot.session
app = Client.from_firefox("my_bot")
```

> **Note:** Works on both native Linux/macOS Firefox profiles and Ubuntu Snap Firefox.

---

## 4. Portable StringSessions (`app.session.to_string()`)

StringSessions serialize your authentication into a single base64 string with the `RubiFlow$` prefix. Ideal for Docker containers, Kubernetes, or cloud VPS where file storage is stateless.

### Exporting a StringSession
```python
import asyncio
from rubiflow import Client

async def export():
    async with Client.from_firefox() as app:
        session_str = app.session.to_string()
        print("Your StringSession:\n", session_str)

asyncio.run(export())
```
Output:
```text
RubiFlow$eyJhdXRoIjoiZndnbmlkb2p0bnFkZGNycXVl...
```

### Loading a StringSession
```python
import os
from rubiflow import Client

session_str = os.environ.get("RUBIFLOW_SESSION")
app = Client(session=session_str)

async def main():
    async with app:
        me = await app.get_me()
        print("Running as:", me.username)

app.run(main())
```

---

## 5. Non-Interactive / Programmatic Login

If you are building a custom web UI or dashboard that performs authentication programmatically, you can disable the terminal prompts (`interactive=False`):

```python
import asyncio
from rubiflow import Client

async def custom_login():
    app = Client("web_user", interactive=False)
    
    # 1. Send SMS code
    res = await app.send_code("09123456789")
    phone_code_hash = res["data"]["phone_code_hash"]

    # 2. Complete sign-in with code received
    sign_res = await app.sign_in("09123456789", phone_code_hash, "123456")
    
    # 3. Check for 2FA if needed
    if sign_res["data"].get("status") == "TwoStepRequired":
        await app.check_two_step_passcode("my_2fa_password")

    # 4. Save session to file
    app.session.save()

asyncio.run(custom_login())
```
