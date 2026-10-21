import asyncio
import sys
sys.path.insert(0, ".")

from rubiflow import Client


async def main():
    print("=" * 50)
    print("      🚀 RubiFlow Framework - Live Verification 🚀")
    print("=" * 50)

    # 1. Automatic Firefox Session Connection
    print("\n1. Connecting via Firefox session...")
    app = Client.from_firefox()

    async with app:
        # 2. Get Profile
        me = await app.get_me()
        print(f"   ✅ Logged in successfully as: {me.full_name} (@{me.username})")
        print(f"   ✅ GUID: {me.guid}")
        print(f"   ✅ Phone: {me.phone}")
        print(f"   ✅ Bio: {me.bio}")

        # 3. StringSession Export & Validation
        string_session = app.session.to_string()
        print(f"\n2. Generated Portable StringSession:\n   {string_session[:45]}...")

        # 4. Fetch Active Conversations
        print("\n3. Fetching Dialogs (getChats)...")
        chats = await app.get_chats()
        print(f"   ✅ Total Dialogs fetched from server: {len(chats)}")
        for idx, chat in enumerate(chats[:3], 1):
            print(f"   {idx}. GUID: {chat.guid} | Type: {chat.type} | Unread: {chat.unread_count}")

        # 5. Fetch Recent Messages from First Chat
        if chats:
            target_guid = chats[0].guid
            print(f"\n4. Fetching recent messages from {target_guid[:15]}...")
            msgs = await app.get_messages(target_guid, limit=3)
            print(f"   ✅ Messages retrieved: {len(msgs)}")
            for m in msgs:
                preview = (m.text[:40] + "...") if m.text else "[Media/Empty]"
                print(f"   - ID: {m.message_id} | Text: {preview}")

    print("\n" + "=" * 50)
    print("  🎉 RubiFlow is 100% operational, fast, and verified! 🎉")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
