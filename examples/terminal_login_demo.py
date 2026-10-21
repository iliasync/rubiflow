"""
RubiFlow - Terminal Interactive Login Demo

Demonstrates how to authenticate using a session file name (or default)
and interactive terminal prompts (Phone Number -> SMS Code -> 2FA Password).
"""

import asyncio
import sys
from rubiflow import Client

async def main():
    # If a session name is passed as CLI argument, use it; otherwise use default ('rubiflow.session')
    session_name = sys.argv[1] if len(sys.argv) > 1 else None

    if session_name:
        print(f"[*] Starting RubiFlow with custom session: '{session_name}'")
        app = Client(session_name)
    else:
        print("[*] Starting RubiFlow with default session ('rubiflow.session')")
        app = Client()

    # When entering context, RubiFlow automatically:
    # 1. Checks if the session file exists and is valid.
    # 2. If not logged in, asks for Phone, SMS Code, and 2FA password in terminal.
    # 3. Saves the session to the session file on disk.
    # 4. Next time you run it, it connects instantly without asking!
    async with app:
        me = await app.get_me()
        print(f"\n🎉 Welcome back, {me.full_name} (@{me.username})!")
        print(f"User GUID : {me.guid}")
        print(f"Phone     : {app.session.phone or 'Hidden'}")
        print(f"Session   : {app.session.file_path}")

        # Send test message to Saved Messages (self)
        try:
            msg = await app.send_message(me.guid, "👋 Hello from RubiFlow Terminal Session!")
            print(f"[+] Sent message to Saved Messages (ID: {msg.message_id})")
        except Exception as exc:
            print(f"[*] Notice: {exc}")

if __name__ == "__main__":
    asyncio.run(main())
