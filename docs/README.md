# ⚡ RubiFlow Documentation

> **Next-Generation High-Performance Async Python Framework for Rubika Messenger & SuperApp**

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.1-0088cc.svg?logo=pypi&logoColor=white)](https://pypi.org/project/rubiflow/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Asyncio](https://img.shields.io/badge/asyncio-powered-purple.svg)](https://docs.python.org/3/library/asyncio.html)

**RubiFlow** is a modern, enterprise-grade, asynchronous framework engineered from the ground up for the Rubika ecosystem. It provides comprehensive, type-hinted access to **300+ methods** spanning the full Rubika Messenger, Rubino Social Network, VOD Movies & Series, and Wallet.

---

## 🚀 Key Highlights

- **⚡ Blazing Fast Asynchronous Core:** Built on top of `aiohttp` with connection pooling, keepalive, and C-accelerated cryptographic primitives (`cryptography`).
- **🛡️ 100% Protocol V6 Compliance:** Automatic AES-256-CBC payload encryption, RSA-SHA256 asymmetric signing, and session character-substitution disguise.
- **🦊 Zero-Code Session Extraction:** Direct auto-import of active web sessions from Firefox without sending SMS verification codes.
- **🌐 Portable StringSessions:** Export lightweight `RubiFlow$...` base64 strings for easy deployment on Docker, Kubernetes, or cloud servers.
- **🤖 Modern Event-Driven Bot Engine:** Decorator-based message dispatching (`@app.on_message()`) with automatic polling and fluent message controls (`await msg.reply()`, `await msg.edit()`).
- **📖 Comprehensive API Documentation:** Full method definitions with parameter tables, types, and return models inspired by the official Telegram Bot API.

---

## 📦 Quick Installation

Install the official package from PyPI:

```bash
pip install rubiflow
```

---

## 💡 10-Second Quickstart

Connect to your account and send your first message:

```python
import asyncio
from rubiflow import Client

async def main():
    # Automatically loads active session from your Firefox browser
    async with Client.from_firefox() as app:
        me = await app.get_me()
        print(f"Logged in as: {me.full_name} (@{me.username})")

        # Send a message
        msg = await app.send_message("u0TargetGuid...", "Hello from RubiFlow! 🚀")
        print("Message ID:", msg.message_id)

asyncio.run(main())
```

---

## 🗺️ Next Steps

- [Installation Guide](installation.md)
- [Authentication & Session Setup](authentication.md)
- [Building Automated Bots](bot_api.md)
- [Complete API Reference](api_reference.md)
