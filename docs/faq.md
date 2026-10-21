# ❓ Frequently Asked Questions (FAQ) & Best Practices

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
