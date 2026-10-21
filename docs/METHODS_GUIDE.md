# RubiFlow Comprehensive Methods & API Guide

Welcome to the **RubiFlow Methods Reference Guide**. This guide provides practical code examples, parameter definitions, and usage patterns for every major category in the RubiFlow framework.

---

## Table of Contents
1. [Client Initialization & Sessions](#1-client-initialization--sessions)
2. [Messaging & Reactions](#2-messaging--reactions)
3. [Dialogs & Chat Management](#3-dialogs--chat-management)
4. [Groups & Voice Chat Spaces](#4-groups--voice-chat-spaces)
5. [Channels & Broadcasts](#5-channels--broadcasts)
6. [Users, Profiles & Contacts](#6-users-profiles--contacts)
7. [Cloud File Storage & CDN](#7-cloud-file-storage--cdn)
8. [Chat Folders & Organization](#8-chat-folders--organization)
9. [Account Settings & Privacy](#9-account-settings--privacy)
10. [Rubino Social Network](#10-rubino-social-network)
11. [VOD Streaming](#11-vod-streaming)
12. [Wallet & Digital Payments](#12-wallet--digital-payments)
13. [Direct Method Invocation (`invoke`)](#13-direct-method-invocation-invoke)

---

## 1. Client Initialization & Sessions

### Connecting with Firefox Active Session
No phone number or SMS verification code is required if you are already logged in to Rubika on Firefox.
```python
from rubiflow import Client

async with Client.from_firefox() as app:
    me = await app.get_me()
    print("Logged in as:", me.full_name)
```

### Exporting and Restoring StringSession
For cloud hosting (Docker, VPS, Heroku) without browser profiles:
```python
# 1. Export
async with Client.from_firefox() as app:
    string_token = app.session.to_string()
    print("StringSession:", string_token)

# 2. Restore anywhere
async with Client(session=string_token) as app:
    me = await app.get_me()
    print("Restored:", me.username)
```

---

## 2. Messaging & Reactions

### Sending Messages
```python
# Simple text message
msg = await app.send_message("u0TargetGuid...", "Hello from RubiFlow!")

# Replying to a message
reply_msg = await app.send_message(
    target="u0TargetGuid...",
    text="Replying to your previous message",
    reply_to_message_id=msg.message_id
)

# Fluent reply directly from Message model
await msg.reply("Another direct reply!")
```

### Editing & Deleting Messages
```python
# Edit text
edited = await app.edit_message("u0TargetGuid...", msg.message_id, "New updated text")
# or fluent:
await msg.edit("New updated text")

# Delete messages (for everyone by default)
await app.delete_messages("u0TargetGuid...", [msg.message_id], delete_for_all=True)
# or fluent:
await msg.delete()
```

### Forwarding Messages
```python
await app.forward_messages(
    from_target="c0ChannelGuid...",
    to_target="g0GroupGuid...",
    message_ids=["1001", "1002"]
)
```

### Reactions (Emojis)
```python
# Add reaction (reaction_id corresponds to emoji catalog)
await app.action_on_message_reaction("u0...", msg.message_id, reaction_id=1, action="Add")

# Remove reaction
await app.action_on_message_reaction("u0...", msg.message_id, reaction_id=1, action="Remove")

# List all available reaction emojis
reactions = await app.get_available_reactions()
for r in reactions:
    print(r["reaction_id"], r["emoji_char"])
```

### Pinned Messages
```python
await app.pin_chat_message("g0GroupGuid...", msg.message_id, notify_members=True)
await app.unpin_chat_message("g0GroupGuid...", msg.message_id)
pinned_msgs = await app.get_pin_message_history("g0GroupGuid...")
```

### Polls
```python
poll_res = await app.create_poll(
    target="g0GroupGuid...",
    question="Which programming language do you prefer?",
    options=["Python", "Go", "Rust", "TypeScript"],
    is_anonymous=True,
    allows_multiple_answers=False
)

# Vote on a poll
await app.vote_poll("g0GroupGuid...", poll_id="...", selection_index=0)
```

---

## 3. Dialogs & Chat Management

### Fetching Conversations
```python
# Fetch active dialogs
chats = await app.get_chats()
for chat in chats:
    print(f"[{chat.type}] {chat.title} (Unread: {chat.unread_count})")

# Fetch specific chats by GUID
specific_chats = await app.get_chats_by_id(["u0...", "c0..."])
```

### Reading & Clearing History
```python
# Mark messages as seen
await app.seen_chats({"u0TargetGuid...": 1945499247262721})

# Clear conversation history
await app.delete_chat_history("u0TargetGuid...")

# Delete dialogs
await app.delete_user_chat("u0...")
await app.delete_group_chat("g0...")
await app.delete_channel_chat("c0...")
```

---

## 4. Groups & Voice Chat Spaces

### Group Management
```python
# Create group
group = await app.add_group(title="Python Devs", member_guids=["u0..."])
group_guid = group["group"]["group_guid"]

# Manage members
await app.add_group_members(group_guid, ["u0User1...", "u0User2..."])
await app.ban_group_member(group_guid, "u0Spammer...")
members = await app.get_group_members(group_guid)

# Admin permissions
await app.set_group_admin(
    group_guid=group_guid,
    member_guid="u0Admin...",
    access_list=["PinMessages", "DeleteMessages", "ChangeInfo"]
)
```

### Voice Chat (Audio Spaces)
```python
# Start voice chat
vc = await app.create_group_voice_chat(group_guid)
vc_id = vc["voice_chat_id"]

# Get participants
participants = await app.get_group_voice_chat(group_guid, vc_id)

# End voice chat
await app.discard_group_voice_chat(group_guid, vc_id)
```

---

## 5. Channels & Broadcasts

```python
# Create channel
channel = await app.add_channel(title="Official News", description="Broadcast channel", channel_type="Public")
channel_guid = channel["channel"]["channel_guid"]

# Invite links
invite_link = await app.create_join_link(channel_guid)
print("Invite link:", invite_link["join_link"])

# Join channel via link
await app.join_channel_by_link("https://rubika.ir/joinc/...")

# Check and update username
if await app.check_channel_username("my_unique_channel"):
    await app.update_channel_username(channel_guid, "my_unique_channel")
```

---

## 6. Users, Profiles & Contacts

```python
# Get current user profile
me = await app.get_me()
print(me.guid, me.phone, me.bio)

# Update profile
await app.update_profile(first_name="Mahan", last_name="Yousefi", bio="RubiFlow Developer")

# Contacts sync
await app.add_address_book(phone="09120000000", first_name="Ali", last_name="Rezaei")
contacts = await app.get_contacts()

# Block / Unblock
await app.block_user("u0...")
await app.unblock_user("u0...")
```

---

## 7. Cloud File Storage & CDN

```python
# Upload local file to Rubika CDN
file_meta = await app.upload_file("photo.jpg")
print(file_meta["file_id"], file_meta["access_hash_rec"])

# Get profile avatars history
avatars = await app.get_avatars(me.guid)
```

---

## 8. Chat Folders & Organization

```python
# Create custom folder
await app.add_folder(
    name="Channels",
    include_chat_types=["Channel"],
    exclude_chat_types=["User", "Group"]
)

# List folders
folders = await app.get_folders()
```

---

## 9. Account Settings & Privacy

```python
# Themes and appearance
appearance = await app.get_appearance_setting()

# Privacy
privacy = await app.get_privacy_setting()

# Stickers
my_stickers = await app.get_my_sticker_sets()
trend_stickers = await app.get_trend_sticker_sets()
```

---

## 10. Rubino Social Network

```python
# Explore feed
explore = await app.get_rubino_explore(limit=24)

# Like and comment
await app.like_post(post_id="...", profile_id="...")
await app.add_comment(post_id="...", profile_id="...", text="Great post!")

# Follow creator
await app.request_follow(target_profile_id="...", action="Follow")

# Stories
stories = await app.get_profiles_stories()
```

---

## 11. VOD Streaming

```python
# Search movies and series
results = await app.search_vod("Inception")

# Get play tokens and HLS stream info
if results:
    media_id = results[0]["media_id"]
    media_info = await app.get_vod_media(media_id)
    play_info = await app.get_vod_play_info(media_id)
```

---

## 12. Wallet & Digital Payments

```python
# Check wallet balance
wallet = await app.get_wallet_status()
print("Balance:", wallet.get("balance"))

# Transfer funds
await app.transfer_credit(recipient_guid="u0...", amount=50000)

# Withdraw to Sheba bank account
await app.cash_out(amount=100000, sheba_iban="123456789012345678901234")
```

---

## 13. Direct Method Invocation (`invoke`)

Any current or future method in Rubika can be invoked dynamically:

```python
result = await app.invoke(
    "sendMessage",
    object_guid="u0TargetGuid...",
    rnd=123456,
    text="Dynamic invoke"
)
print("Invoke status:", result.get("status"))
```
