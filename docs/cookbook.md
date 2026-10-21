# 🍳 RubiFlow Cookbook & Practical Recipes

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

ANNOUNCEMENT = """
🔥 **RubiFlow Update Released!**

Version 1.0.1 is now live on PyPI with:
- Pyrogram-style session naming
- Terminal interactive login
- Robust 2FA password handling

Install now: `pip install --upgrade rubiflow`
"""

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
