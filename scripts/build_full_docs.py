"""
Comprehensive Documentation Builder for RubiFlow.
Generates exhaustive, Telegram Bot API-grade documentation across all categories.
"""

import os

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))

def save_doc(filename: str, content: str):
    path = os.path.join(DOCS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {filename} ({len(content.splitlines())} lines)")

# ==============================================================================
# _sidebar.md
# ==============================================================================
sidebar_md = """- **Getting Started**
  - [Introduction](README.md)
  - [Installation Guide](installation.md)
  - [Authentication & Sessions](authentication.md)
  - [Building Bots (Event API)](bot_api.md)

- **Data Models & Types**
  - [Available Types](types.md)
  - [Errors & Exceptions](errors.md)

- **Complete API Reference**
  - [API Overview](api_reference.md)
  - [Messaging & Polls](methods_messages.md)
  - [Chats & Dialogs](methods_chats.md)
  - [Groups & Voice Chats](methods_groups.md)
  - [Channels & Broadcasts](methods_channels.md)
  - [Users & Contacts](methods_users.md)
  - [Cloud Files & CDN](methods_files.md)
  - [Folders & Organization](methods_folders.md)
  - [Settings, 2FA & Privacy](methods_settings.md)
  - [Rubino Social Network](methods_rubino.md)
  - [VOD Movies & Series](methods_vod.md)
  - [Wallet & Payments](methods_wallet.md)
  - [Direct Invoker (`invoke`)](methods_invoker.md)

- **Cookbook & Best Practices**
  - [Recipes & Practical Bots](cookbook.md)
  - [FAQ & Architecture](faq.md)

- **Deep Dive**
  - [V6 Cryptography & Security](cryptography.md)
  - [All 301 Methods Catalog](RUBIKA_API_FULL_REFERENCE.md)
"""

# ==============================================================================
# types.md
# ==============================================================================
types_md = """# 📦 Available Types & Data Models

This page describes all core data models, structures, and helper classes used throughout RubiFlow. All objects are strongly typed, dataclass-backed, and provide convenient serialization and manipulation helpers.

---

## `User`
Represents a Rubika user profile account.

### Fields
| Field | Type | Description |
| :--- | :--- | :--- |
| `guid` | `str` | Unique 32-character global identifier of the user (starts with `u0`). |
| `first_name` | `str` | First name of the user. |
| `last_name` | `Optional[str]` | Last name of the user, if set. |
| `username` | `Optional[str]` | Public handle without `@` symbol, if reserved. |
| `phone` | `Optional[str]` | Phone number in international format (only visible if allowed by privacy). |
| `bio` | `Optional[str]` | About text / biography (up to 70 characters). |
| `is_online` | `bool` | Whether the user is currently online on Rubika. |
| `last_online` | `Optional[int]` | Unix timestamp of when the user was last active. |
| `avatar_thumbnail` | `Optional[str]` | Base64-encoded micro thumbnail of avatar. |
| `raw` | `Dict[str, Any]` | Complete raw dictionary payload returned by the Rubika RPC server. |

### Properties
- `full_name` (`str`): Returns combined `"first_name last_name"`, stripping extra spaces.

#### Example
```python
user = await app.get_user_info("u0ABCDEF123456789")
print(f"Name: {user.full_name} (@{user.username})")
print(f"Online: {user.is_online}")
```

---

## `Chat`
Represents a conversation dialog (private chat, supergroup, or broadcast channel).

### Fields
| Field | Type | Description |
| :--- | :--- | :--- |
| `guid` | `str` | Unique GUID of the chat (`u...` for user, `g...` for group, `c...` for channel). |
| `title` | `str` | Title of the group, channel, or the contact's full name. |
| `chat_type` | `str` | Type identifier: `'User'`, `'Group'`, or `'Channel'`. |
| `count_unseen` | `int` | Number of unread messages waiting in this chat. |
| `last_message` | `Optional[Message]` | Most recent message received or sent in this dialog. |
| `pinned_message_id` | `Optional[str]` | Message ID of the currently pinned message, if any. |
| `time` | `int` | Unix timestamp of the last activity in the chat. |
| `raw` | `Dict[str, Any]` | Raw server response dictionary. |

### Properties
- `unread_count` (`int`): Alias for `count_unseen`.
- `is_user` (`bool`): `True` if `chat_type == 'User'`.
- `is_group` (`bool`): `True` if `chat_type == 'Group'`.
- `is_channel` (`bool`): `True` if `chat_type == 'Channel'`.

#### Example
```python
chats = await app.get_chats(limit=20)
for chat in chats:
    if chat.unread_count > 0:
        print(f"[{chat.chat_type}] {chat.title}: {chat.unread_count} unread messages")
```

---

## `Message`
Represents a message sent or received in any conversation.

### Fields
| Field | Type | Description |
| :--- | :--- | :--- |
| `message_id` | `str` | Unique identifier of the message inside the chat. |
| `chat_guid` | `str` | GUID of the chat (user, group, or channel) where message belongs. |
| `author_guid` | `str` | GUID of the user or channel that authored the message. |
| `text` | `str` | Text content of the message (empty string for media without caption). |
| `time` | `int` | Unix timestamp of when the message was sent. |
| `reply_to_message_id` | `Optional[str]` | Identifier of original message being replied to, if any. |
| `is_edited` | `bool` | `True` if message has been edited after transmission. |
| `raw` | `Dict[str, Any]` | Full raw message dictionary from Rubika. |

### Bound Async Methods
Every `Message` object received inside `@app.on_message()` or fetched via API has bound convenience methods:

#### `await msg.reply(text: str) -> Message`
Sends a reply quoting this exact message.
```python
@app.on_message()
async def handler(msg: Message):
    if msg.text == "/help":
        await msg.reply("Here is the help manual!")
```

#### `await msg.edit(new_text: str) -> Dict[str, Any]`
Edits the text of this message (if authored by self).
```python
sent = await app.send_message("u0...", "Processing...")
await asyncio.sleep(1)
await sent.edit("Finished processing!")
```

#### `await msg.delete(delete_for_all: bool = True) -> Dict[str, Any]`
Deletes this message.
```python
if "spam_word" in msg.text:
    await msg.delete()
```

#### `await msg.forward(to_chat: str) -> Dict[str, Any]`
Forwards this message to another chat GUID.
```python
await msg.forward("c0ArchiveChannelGUID...")
```

---

## `Session`
Represents the cryptographic identity and credentials of an authenticated Rubika session.

### Fields & Properties
| Attribute | Type | Description |
| :--- | :--- | :--- |
| `auth` | `str` | Permanent 32-character authentication token string. |
| `private_key_pem` | `str` | RSA private key in standard PEM format. |
| `dc_url` | `str` | Data Center endpoint URL (e.g. `https://messengerg2c332.iranlms.ir`). |
| `user_guid` | `Optional[str]` | Authenticated account GUID. |
| `phone` | `Optional[str]` | Authenticated phone number. |
| `is_authenticated` | `bool` | `True` if session has valid server auth credentials. |
| `file_path` | `Optional[str]` | Associated local session file path on disk (e.g. `bot.session`). |

### Methods
- `session.to_string() -> str`: Encodes session to portable base64 string (`RubiFlow$...`).
- `Session.from_string(session_string: str) -> Session`: Deserializes StringSession.
- `session.save(file_path: Optional[str] = None)`: Writes session to file.
- `Session.load_from_file(file_path: str) -> Session`: Loads session from JSON file.
- `Session.from_firefox() -> Session`: Decrypts active Firefox browser session.
- `Session.new_temporary(...) -> Session`: Creates unauthenticated temporary session for login.

---

## `FileMetadata`
Dictionary returned when requesting or completing file uploads via `upload_file`.

```python
{
    "file_id": "1049285712",
    "access_hash_send": "349102847501928471029384",
    "mime": "image/jpeg",
    "size": 245892,
    "file_name": "photo.jpg",
    "cdn_url": "https://storage.iranlms.ir/..."
}
```
"""

# ==============================================================================
# errors.md
# ==============================================================================
errors_md = """# ⚠️ Errors & Exception Handling

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
"""

# ==============================================================================
# cookbook.md
# ==============================================================================
cookbook_md = """# 🍳 RubiFlow Cookbook & Practical Recipes

Production-ready patterns, automation recipes, and advanced bot implementations using RubiFlow.

---

## Recipe 1: Smart Group Auto-Moderator (Anti-Link & Anti-Spam)

Automatically deletes messages containing unauthorized links or forbidden keywords and warns the sender:

```python
import re
from rubiflow import Client, Message

app = Client("group_moderator")

LINK_PATTERN = re.compile(r"(https?://|t\.me/|rubika\.ir/|rubika://)", re.IGNORECASE)
BAD_WORDS = {"spamword1", "badword2", "advertisement"}

@app.on_message()
async def auto_moderator(msg: Message):
    # Only monitor groups (GUIDs starting with 'g0')
    if not msg.chat_guid.startswith("g0"):
        return

    text = msg.text or ""

    # Check for forbidden links
    if LINK_PATTERN.search(text):
        await msg.delete()
        warning = await app.send_message(
            msg.chat_guid,
            f"⚠️ Warning: Links are not allowed in this group!"
        )
        return

    # Check for forbidden words
    if any(bw in text.lower() for bw in BAD_WORDS):
        await msg.delete()
        print(f"[Moderator] Deleted spam from {msg.author_guid}")

if __name__ == "__main__":
    print("Auto-moderator bot running...")
    app.run()
```

---

## Recipe 2: Channel Post Scheduler & Broadcaster

Broadcasts formatted announcements to multiple channels or groups with rate-limiting protection:

```python
import asyncio
from rubiflow import Client

TARGET_CHANNELS = [
    "c0Channel1GUID...",
    "c0Channel2GUID...",
    "g0Group1GUID...",
]

ANNOUNCEMENT = \"\"\"
🔥 **RubiFlow Update Released!**

Version 1.0.0 is now live on PyPI with:
- Pyrogram-style session naming
- Terminal interactive login
- Robust 2FA password handling

Install now: `pip install --upgrade rubiflow`
\"\"\"

async def broadcast():
    async with Client("broadcaster") as app:
        for idx, target in enumerate(TARGET_CHANNELS, 1):
            try:
                msg = await app.send_message(target, ANNOUNCEMENT)
                print(f"[{idx}/{len(TARGET_CHANNELS)}] Broadcasted to {target} (Msg ID: {msg.message_id})")
            except Exception as exc:
                print(f"[!] Failed to send to {target}: {exc}")
            
            # Anti-flood sleep
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(broadcast())
```

---

## Recipe 3: Rubino Social Explorer & Auto-Liker

Searches a hashtag on Rubino and automatically likes the latest posts:

```python
import asyncio
from rubiflow import Client

async def rubino_bot():
    async with Client("rubino_user") as app:
        print("[*] Searching posts with hashtag #python...")
        results = await app.search_rubino_hashtag("python")
        
        posts = results.get("posts", [])
        print(f"[+] Found {len(posts)} posts.")

        for post in posts[:5]:
            post_id = post["id"]
            profile_id = post["profile"]["id"]
            author = post["profile"].get("username", "Unknown")

            print(f"[*] Liking post {post_id} by @{author}...")
            await app.like_post(post_id=post_id, profile_id=profile_id)
            await asyncio.sleep(3)

        print("[+] Finished liking explore posts!")

if __name__ == "__main__":
    asyncio.run(rubino_bot())
```

---

## Recipe 4: Running 24/7 as a Linux `systemd` Service

Create a systemd unit file to keep your bot running indefinitely on a VPS:

### `/etc/systemd/system/rubiflow-bot.service`
```ini
[Unit]
Description=RubiFlow Telegram-Style Automated Bot
After=network.target

[Service]
Type=simple
User=mahan
WorkingDirectory=/home/mahan/my-bot
ExecStart=/usr/bin/python3 /home/mahan/my-bot/main.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable rubiflow-bot
sudo systemctl start rubiflow-bot
sudo journalctl -u rubiflow-bot -f
```

---

## Recipe 5: Running Along Web Server (FastAPI / aiohttp)

You can run RubiFlow inside a FastAPI web application to trigger messages via HTTP webhooks:

```python
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from rubiflow import Client

rubi_app = Client("web_api_bot", interactive=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to Rubika
    await rubi_app.start()
    yield
    # Shutdown: close transport
    await rubi_app.stop()

api = FastAPI(lifespan=lifespan)

@api.post("/send_alert")
async def send_alert(target: str, text: str):
    try:
        msg = await rubi_app.send_message(target, text)
        return {"ok": True, "message_id": msg.message_id}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
```
"""

# ==============================================================================
# faq.md
# ==============================================================================
faq_md = """# ❓ Frequently Asked Questions (FAQ) & Best Practices

---

### Q1: Why can't I use Telethon or Pyrogram directly with Rubika?
**A:** While Rubika's UI is inspired by Telegram, its underlying network protocol and transport are completely custom:
- Telegram uses MTProto binary serialization over TCP port 443 with Diffie-Hellman key exchanges.
- Rubika uses **Protocol V6 JSON over HTTPS POST** with custom derived 32-character AES passphrases, AES-256-CBC encryption with zero IVs, RSA-SHA256 asymmetric signing, and character substitution disguise tables (`em` cipher).
RubiFlow implements these Rubika-specific primitives natively while providing a clean Pyrogram-like high-level API.

---

### Q2: Where are session files saved?
**A:** By default, sessions are saved as `<name>.session` (or `rubiflow.session` if unnamed) in your current working directory. You can also specify an absolute path or relative path, e.g.:
```python
app = Client("/var/lib/my_app/sessions/account_1.session")
```
RubiFlow automatically creates parent directories if they don't exist.

---

### Q3: How do I manage multiple accounts concurrently?
**A:** Simply instantiate multiple `Client` instances with distinct session names:

```python
import asyncio
from rubiflow import Client

async def main():
    bot1 = Client("bot_support")
    bot2 = Client("bot_notifier")

    async with bot1, bot2:
        me1 = await bot1.get_me()
        me2 = await bot2.get_me()
        print(f"Bot 1: @{me1.username} | Bot 2: @{me2.username}")

        # Both can poll or send messages concurrently
        await asyncio.gather(
            bot1.send_message("u0...", "From Bot 1"),
            bot2.send_message("u0...", "From Bot 2")
        )

asyncio.run(main())
```

---

### Q4: What is the maximum message length?
**A:** Rubika supports up to **4096 UTF-8 characters** per text message. If your text exceeds 4096 characters, chunk it into smaller blocks:

```python
def chunk_text(text: str, limit: int = 4000):
    return [text[i:i+limit] for i in range(0, len(text), limit)]

for chunk in chunk_text(long_text):
    await app.send_message(target, chunk)
    await asyncio.sleep(0.5)
```

---

### Q5: How do I avoid being rate limited (banned / flood wait)?
1. **Add Delays:** Always add `await asyncio.sleep(1.0)` to `2.0` between bulk broadcast messages.
2. **Handle Exceptions:** Catch `ApiError` and inspect `exc.status_det == "TOO_MANY_REQUESTS"`.
3. **Use Connection Pooling:** RubiFlow's `AsyncTransport` automatically reuses TCP connections via HTTP keep-alive, significantly reducing network overhead and handshake frequency.
"""

# ==============================================================================
# methods_settings.md (Expanded)
# ==============================================================================
methods_settings_md = """# ⚙️ Settings, 2FA & Privacy API

Complete reference for managing account security, Two-Step Verification (2FA), privacy visibility, themes, and active device sessions.

---

### `setup_two_step_verification`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Enables Two-Step Verification by setting a master password. Once enabled, logging into the account requires entering this password after the SMS code.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `password` | `str` | Yes | - | Master password to be set. |
| `hint` | `str` | No | `None` | Optional password hint to remind the user. |
| `recovery_email` | `str` | No | `None` | Optional recovery email to reset password if forgotten. |

#### Code Example
```python
await app.setup_two_step_verification(
    password="super_secure_password_123",
    hint="Favorite book character",
    recovery_email="user@example.com"
)
```

---

### `check_two_step_passcode`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Validates the user's Two-Step Verification password during login or when confirming sensitive operations.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `password` | `str` | Yes | - | Account 2FA password. |

#### Return Value
```json
{
  "status": "OK",
  "data": {
    "auth": "permanent_auth_token_32chars...",
    "user": {
      "user_guid": "u0ABCDEF1234567890",
      "first_name": "Mahan"
    }
  }
}
```

---

### `change_password`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Changes an existing Two-Step Verification password.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `old_password` | `str` | Yes | - | The current 2FA password. |
| `new_password` | `str` | Yes | - | The new 2FA password. |
| `hint` | `str` | No | `None` | New password hint. |

---

### `set_recovery_email` / `verify_recovery_email`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`set_recovery_email(email: str)`**: Requests sending a verification code to a recovery email address.
- **`verify_recovery_email(email_code: str)`**: Confirms the received verification code to bind the recovery email.

---

### `get_privacy_settings` / `set_privacy_setting`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Queries or modifies who can see your last seen status, profile photos, phone number, or add you to groups.

#### Options
Allowed visibility rules: `'Everybody'`, `'MyContacts'`, `'Nobody'`.

#### Code Example
```python
# Get current privacy rules
privacy = await app.get_privacy_settings()
print(privacy)

# Update last seen to contacts only
await app.set_privacy_setting({
    "last_seen_type": "MyContacts",
    "phone_number_type": "Nobody"
})
```

---

### `get_notification_settings` / `set_notification_setting`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Controls push notifications, sound, vibration, and message previews for Private Chats, Groups, and Channels.

#### Code Example
```python
await app.set_notification_setting({
    "users_mute": False,
    "groups_mute": True,
    "channels_mute": True
})
```

---

### `get_appearance_settings` / `set_appearance_setting`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Controls app color themes (Dark, Light, System) and message bubble font scale.

---

### Active Sessions Management

- **`get_my_sessions() -> List[Dict[str, Any]]`**: Retrieves a list of all active sessions, including device model, IP address, system version, and last active timestamp.
- **`terminate_session(session_key: str)`**: Terminates a specific device session by its unique session key.
- **`terminate_user_sessions()`**: Terminates all other logged-in sessions except the current one.
"""

# ==============================================================================
# methods_rubino.md (Expanded)
# ==============================================================================
methods_rubino_md = """# 📸 Rubino Social Network API

Comprehensive reference for interacting with Rubino, Rubika's built-in Instagram-style social media platform.

---

### `get_rubino_explore`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Fetches the infinite-scroll Explore feed containing popular photos, videos, and reels.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | No | `24` | Number of explore posts to retrieve. |
| `max_id` | `str` | No | `None` | Cursor for pagination offset. |

#### Code Example
```python
explore = await app.get_rubino_explore(limit=10)
for post in explore.get("posts", []):
    profile = post.get("profile", {})
    print(f"Post {post['id']} by @{profile.get('username')}: {post.get('caption')}")
```

---

### `get_rubino_profile_info`
<span class="badge badge-post">POST</span> <span class="badge async">Async</span>

Fetches complete public information about a creator profile on Rubino.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `profile_id` | `str` | Yes | - | Unique profile ID of the creator. |

#### Return Value
```json
{
  "profile": {
    "id": "p0ABCDEF...",
    "username": "creator_name",
    "name": "Mahan",
    "bio": "Developer and Content Creator",
    "count_followers": 1420,
    "count_following": 250,
    "count_posts": 45,
    "is_private": false,
    "is_verified": true
  }
}
```

---

### `get_rubino_profile_posts`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Retrieves a creator's published grid posts with pagination.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `profile_id` | `str` | Yes | - | Creator profile ID. |
| `limit` | `int` | No | `20` | Maximum number of posts to fetch. |
| `max_id` | `str` | No | `None` | Pagination cursor. |

---

### `like_post` / `unlike_post`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Likes or un-likes a post on Rubino.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `post_id` | `str` | Yes | - | Unique identifier of the post. |
| `profile_id` | `str` | Yes | - | Profile ID of the post author. |

#### Code Example
```python
await app.like_post(post_id="12345678", profile_id="p0ABCDEF...")
```

---

### `bookmark_post` / `unbookmark_post`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Saves or removes a post from your private saved bookmarks collection.

---

### `add_comment` / `like_comment` / `get_comments`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`add_comment(post_id: str, profile_id: str, content: str)`**: Submits a text comment on a post.
- **`like_comment(comment_id: str, post_id: str, profile_id: str)`**: Likes a specific comment.
- **`get_comments(post_id: str, profile_id: str, limit: int = 20)`**: Fetches comments list with author details.

---

### `request_follow`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Follows or unfollows a creator profile.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `target_profile_id` | `str` | Yes | - | Target profile to follow. |
| `action` | `str` | No | `'Follow'` | `'Follow'` or `'Unfollow'`. |

---

### `get_story` / `get_story_viewers`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`get_story(story_id: str, profile_id: str)`**: Fetches media URL, duration, and viewers counter for a story.
- **`get_story_viewers(story_id: str, profile_id: str)`**: Lists users who have viewed your story.

---

### `search_rubino_profile` / `search_rubino_hashtag`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`search_rubino_profile(search_text: str)`**: Searches creators by username or display name.
- **`search_rubino_hashtag(search_text: str)`**: Searches posts tagged with a specific hashtag without `#`.
"""

# ==============================================================================
# methods_vod.md (Expanded)
# ==============================================================================
methods_vod_md = """# 🎬 VOD Movies & Series API

Access Rubika's streaming entertainment platform: search movies and series, fetch HLS video stream playlists (`.m3u8`), manage watchlists, and view cast filmographies.

---

### `search_vod`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Searches the Rubika VOD video library.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `query` | `str` | Yes | - | Title, actor, or genre search term. |

#### Return Value
```python
results = await app.search_vod("Interstellar")
for item in results:
    print(f"Title: {item['title']} | Type: {item['type']} | ID: {item['id']}")
```

---

### `get_vod_media`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Retrieves full metadata for a movie or TV series.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `media_id` | `str` | Yes | - | Unique media identifier. |

#### Response Attributes
Includes synopsis, genres, duration, release year, IMDb rating, age rating, and thumbnail covers.

---

### `get_vod_play_info`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Returns direct HLS streaming playlist URLs (`.m3u8`), playback tokens, available resolutions (1080p, 720p, 480p, 360p), and subtitle tracks.

#### Code Example
```python
play_info = await app.get_vod_play_info("media_12345")
print(f"HLS Master Playlist: {play_info.get('play_url')}")
```

---

### `get_vod_season_episodes`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Lists all episodes and season breakdowns for a TV show.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `series_id` | `str` | Yes | - | Unique identifier of the TV show. |
| `season_id` | `str` | No | `None` | Optional season filter. |

---

### `get_vod_wishlist` / `add_vod_wishlist`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`get_vod_wishlist()`**: Lists all movies and shows saved to the user's watchlist.
- **`add_vod_wishlist(media_id: str)`**: Adds a title to the watchlist.

---

### `set_vod_play_time`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Synchronizes playback progress (resume point in seconds) across devices.
"""

# ==============================================================================
# methods_wallet.md (Expanded)
# ==============================================================================
methods_wallet_md = """# 💳 Wallet & Payments API

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
"""

# ==============================================================================
# methods_folders.md (Expanded)
# ==============================================================================
methods_folders_md = """# 🗂️ Folders & Organization API

Methods for creating, retrieving, and organizing custom chat folders and filter tabs like Telegram.

---

### `get_folders`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Retrieves all configured chat folders for the user's account.

#### Return Value
Returns a list of folder dictionaries:
```python
folders = await app.get_folders()
for folder in folders:
    print(f"Folder: {folder.get('name')} (ID: {folder.get('folder_id')})")
```

---

### `create_folder`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Creates a new custom chat tab.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `str` | Yes | - | Tab title (e.g. `'Work'`, `'Channels'`, `'Bots'`). |
| `include_chat_types` | `List[str]` | Yes | - | Chat categories to include: `['Users', 'Groups', 'Channels', 'Bots']`. |
| `exclude_chat_types` | `List[str]` | No | `None` | Optional chat categories to exclude. |

#### Code Example
```python
await app.create_folder(
    name="Channels",
    include_chat_types=["Channels"]
)
```

---

### `delete_folder`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Deletes a chat folder by its unique ID.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `folder_id` | `str` | Yes | - | Folder identifier. |
"""

# Save all docs
docs_to_save = {
    "_sidebar.md": sidebar_md,
    "types.md": types_md,
    "errors.md": errors_md,
    "cookbook.md": cookbook_md,
    "faq.md": faq_md,
    "methods_settings.md": methods_settings_md,
    "methods_rubino.md": methods_rubino_md,
    "methods_vod.md": methods_vod_md,
    "methods_wallet.md": methods_wallet_md,
    "methods_folders.md": methods_folders_md,
}

for filename, content in docs_to_save.items():
    save_doc(filename, content)

print("Documentation expansion builder finished successfully!")
