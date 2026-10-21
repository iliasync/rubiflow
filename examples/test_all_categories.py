import asyncio
import sys
sys.path.insert(0, ".")

from rubiflow import Client


async def main():
    print("=" * 60)
    print("      🧪 Testing RubiFlow Comprehensive API Coverage 🧪")
    print("=" * 60)

    app = Client.from_firefox()
    async with app:
        # 1. Auth & Session Methods
        print("\n[1] Testing Auth & Session Methods...")
        sessions = await app.get_my_sessions()
        print(f"    ✅ Active Device Sessions fetched: {len(sessions)}")

        # 2. Users & Profile Methods
        print("\n[2] Testing Users & Profile Methods...")
        me = await app.get_me()
        print(f"    ✅ Current Account: {me.full_name} (@{me.username})")
        avail = await app.check_user_username("rubiflow_unique_user_9988")
        print(f"    ✅ Username Availability Check: {'Available' if avail else 'Taken'}")

        # 3. Chats & Messaging Methods
        print("\n[3] Testing Chats & Messaging Methods...")
        chats = await app.get_chats()
        print(f"    ✅ Total Dialogs fetched: {len(chats)}")
        
        if chats:
            by_id = await app.get_chats_by_id([chats[0].guid])
            print(f"    ✅ Specific Chat by ID fetched: {len(by_id)} chat(s)")

        reactions = await app.get_available_reactions()
        print(f"    ✅ Available Emoji Reactions: {len(reactions)} emojis")
        
        drafts = await app.get_all_drafts()
        print(f"    ✅ Cloud Synced Drafts: {len(drafts)}")

        # 4. Message History Retrieval
        if chats:
            first_chat = chats[0]
            print(f"\n[4] Testing Message History from {first_chat.guid[:15]}...")
            msgs = await app.get_messages(first_chat.guid, limit=3)
            print(f"    ✅ Messages retrieved: {len(msgs)}")
            for m in msgs:
                txt = (m.text[:35] + "...") if m.text else "[Media]"
                print(f"       - ID: {m.message_id} | {txt}")

        # 5. Folders & Organization
        print("\n[5] Testing Folders Methods...")
        folders = await app.get_folders()
        print(f"    ✅ User Chat Folders/Tabs: {len(folders)}")

        # 6. Settings & Appearance Methods
        print("\n[6] Testing Settings Methods...")
        appearance = await app.get_appearance_setting()
        print(f"    ✅ Font Size: {appearance.get('font_size', 'Default')} | Theme: {appearance.get('theme', 'Default')}")
        privacy = await app.get_privacy_setting()
        print(f"    ✅ Privacy Settings keys: {len(privacy)}")
        stickers = await app.get_my_sticker_sets()
        print(f"    ✅ Installed Sticker Sets: {len(stickers)}")

        # 7. Raw Method Invoker (invoke)
        print("\n[7] Testing Raw 'invoke' Engine...")
        raw_res = await app.invoke("getUserInfo", user_guid=me.guid)
        print(f"    ✅ Raw Invoke 'getUserInfo': {raw_res.get('status')} (user: {raw_res.get('data', {}).get('user', {}).get('username')})")

    print("\n" + "=" * 60)
    print("  🎉 All Categories Executed Successfully with 0 Errors! 🎉")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
