# 🤖 Bot API & Event-Driven Engine

RubiFlow includes a high-performance, asynchronous event dispatching engine inspired by Telegram bot frameworks like **Pyrogram** and **aiogram**.

---

## 1. Quick Echo Bot

```python
from rubiflow import Client, Message

app = Client.from_firefox()

@app.on_message()
async def echo_handler(msg: Message):
    # Avoid infinite loops by ignoring self messages
    if msg.author_guid == app._me.guid:
        return

    if msg.text == "/start":
        await msg.reply("Welcome to RubiFlow Bot! 🚀\nSend me any text and I will echo it.")
    else:
        await msg.reply(f"Echo: {msg.text}")

if __name__ == "__main__":
    print("Bot is listening for messages...")
    app.run()
```

---

## 2. The `Message` Object

Incoming messages passed to `@app.on_message()` are instances of `rubiflow.models.Message`:

### Attributes
- `msg.message_id`: Unique identifier of the message (`str`).
- `msg.chat_guid`: GUID of the chat (user, group, or channel).
- `msg.author_guid`: GUID of the user who sent the message.
- `msg.text`: Text content of the message.
- `msg.raw`: Complete dictionary returned by Rubika server.

### Bound Helper Methods
Instead of calling `app.send_message(...)` manually, you can use convenient methods on the message instance:

#### `await msg.reply(text)`
Sends a reply directly quoting this message.
```python
await msg.reply("This is a direct reply!")
```

#### `await msg.delete()`
Deletes this message for everyone in the chat.
```python
await msg.delete()
```

#### `await msg.forward(to_chat)`
Forwards this message to another chat.
```python
await msg.forward("g0ABCDEF123456789")
```

---

## 3. Command Routing & Filtering

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
        await msg.reply(
            "Available commands:\n"
            "/info - Show chat ID\n"
            "/ping - Check bot response\n"
            "/echo <text> - Echo back"
        )

    elif text == "/ping":
        await msg.reply("Pong! 🏓")

    elif text.startswith("/echo "):
        echo_content = text.split("/echo ", 1)[1]
        await msg.reply(echo_content)

app.run()
```

---

## 4. Running Concurrent Background Tasks

You can run continuous tasks (e.g. data scrapers, periodic broadcasts, or health checks) alongside the bot polling engine:

```python
import asyncio
from rubiflow import Client, Message

app = Client.from_firefox()

@app.on_message()
async def on_message(msg: Message):
    if msg.text == "/status":
        await msg.reply("All systems operational.")

async def periodic_broadcast():
    while True:
        await asyncio.sleep(3600)  # Every hour
        print("Running hourly sync...")

async def main():
    async with app:
        asyncio.create_task(periodic_broadcast())
        await app._polling_loop()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5. Production Server Deployment

1. Export your session once:
   ```python
   session_str = app.session.to_string()
   print(session_str)
   ```
2. Store it as an environment variable (`RUBIFLOW_SESSION`) on your server.
3. Launch with `systemd` or Docker:
   ```python
   import os
   from rubiflow import Client

   app = Client(session=os.environ["RUBIFLOW_SESSION"])

   @app.on_message()
   async def handler(msg):
       await msg.reply("Running on production VPS!")

   app.run()
   ```
