# 🤖 Building Bots & Event Handlers with RubiFlow

RubiFlow provides an event-driven bot engine inspired by modern Telegram libraries (Pyrogram, Telethon, aiogram), enabling you to create automated bots, responders, and moderation tools in Python.

---

## 1. Quick Echo Bot

```python
from rubiflow import Client, Message

app = Client.from_firefox()

@app.on_message()
async def echo_handler(msg: Message):
    # Ignore messages sent by ourselves
    if msg.author_guid == app._me.guid:
        return

    if msg.text == "/start":
        await msg.reply("Welcome to RubiFlow Bot! 🚀\nSend any text and I will echo it back.")
    else:
        await msg.reply(f"You said: {msg.text}")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
```

---

## 2. Command Filtering & Routing

```python
from rubiflow import Client, Message

app = Client.from_firefox()

@app.on_message()
async def command_router(msg: Message):
    text = (msg.text or "").strip()

    if text.startswith("/info"):
        chat_info = f"Chat GUID: `{msg.chat_guid}`\nMessage ID: `{msg.message_id}`"
        await msg.reply(chat_info)

    elif text.startswith("/help"):
        await msg.reply("Available commands:\n/info - Show chat ID\n/ping - Check latency")

    elif text == "/ping":
        await msg.reply("Pong! 🏓")

app.run()
```

---

## 3. Running Background Tasks Along with the Bot

You can run your own asynchronous background coroutines (e.g. periodically broadcasting messages or syncing data) alongside the bot:

```python
import asyncio
from rubiflow import Client, Message

app = Client.from_firefox()

@app.on_message()
async def on_message(msg: Message):
    if msg.text == "hi":
        await msg.reply("Hello!")

async def periodic_status():
    while True:
        await asyncio.sleep(3600)
        print("Bot is alive and healthy.")

async def main():
    async with app:
        # Schedule periodic task
        asyncio.create_task(periodic_status())
        # Start polling loop
        await app._polling_loop()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. Deploying to Cloud Servers

1. Export your session once using `app.session.to_string()`.
2. Set the `RUBIFLOW_SESSION` environment variable on your server.
3. Run your bot headlessly:

```python
import os
from rubiflow import Client

session_str = os.environ.get("RUBIFLOW_SESSION")
app = Client(session=session_str)

@app.on_message()
async def handler(msg):
    await msg.reply("Hello from Cloud VPS!")

app.run()
```
