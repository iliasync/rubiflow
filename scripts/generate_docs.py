"""
Generator script to build Telegram Bot API-styled Markdown documentation
for the RubiFlow framework.
"""

import os

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))

def write_doc(filename: str, content: str):
    path = os.path.join(DOCS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

# ==============================================================================
# 1. API Reference Overview (docs/api_reference.md)
# ==============================================================================
api_reference_md = """# 📚 RubiFlow API Reference

Welcome to the **RubiFlow API Reference**. This documentation follows the structure and style of the official [Telegram Bot API](https://core.telegram.org/bots/api), presenting every method with input parameters, types, required flags, return structures, and ready-to-run asynchronous Python code samples.

---

## Architecture Overview

All methods are exposed directly through the high-level `rubiflow.Client` class via modular Python mixins:

```
                            ┌─────────────────────┐
                            │   rubiflow.Client   │
                            └──────────┬──────────┘
       ┌───────────────────────────────┼───────────────────────────────┐
       │                               │                               │
┌──────▼────────┐              ┌───────▼────────┐              ┌───────▼────────┐
│MessagesMethods│              │  ChatsMethods  │              │ GroupsMethods  │
└───────────────┘              └────────────────┘              └────────────────┘
       │                               │                               │
┌──────▼────────┐              ┌───────▼────────┐              ┌───────▼────────┐
│ChannelsMethods│              │  UsersMethods  │              │  FilesMethods  │
└───────────────┘              └────────────────┘              └────────────────┘
       │                               │                               │
┌──────▼────────┐              ┌───────▼────────┐              ┌───────▼────────┐
│FoldersMethods │              │SettingsMethods │              │ RubinoMethods  │
└───────────────┘              └────────────────┘              └────────────────┘
       │                               │                               │
┌──────▼────────┐              ┌───────▼────────┐              ┌───────▼────────┐
│  VodMethods   │              │ WalletMethods  │              │  AuthMethods   │
└───────────────┘              └────────────────┘              └────────────────┘
```

---

## Navigation & Categories

| Category | Description | Methods Count |
| :--- | :--- | :--- |
| [Messaging & Polls](methods_messages.md) | Sending, editing, deleting, forwarding, searching messages, pinning, and interactive polls. | 13 methods |
| [Chats & Dialogs](methods_chats.md) | Dialog list retrieval, unread indicators, chat metadata, and clearing history. | 5 methods |
| [Groups & Voice Chats](methods_groups.md) | Supergroup management, member roles, bans, default permissions, and WebRTC voice chats. | 11 methods |
| [Channels & Broadcasts](methods_channels.md) | Channel creation, subscribers, admin permissions, and public username management. | 9 methods |
| [Users & Contacts](methods_users.md) | Profile inspection, blocking/unblocking, address book contacts, and @username reservation. | 11 methods |
| [Cloud Files & CDN](methods_files.md) | Uploading, downloading, chunked streaming across Rubika CDN nodes, and sticker packs. | 5 methods |
| [Folders & Organization](methods_folders.md) | Custom dialog folders and filter rules (Personal, Groups, Channels, Bots). | 3 methods |
| [Settings & Privacy](methods_settings.md) | Profile visibility, two-step verification, appearance themes, and active session termination. | 8 methods |
| [Rubino Social Network](methods_rubino.md) | Instagram-style social network: feed explore, likes, comments, stories, and following. | 16 methods |
| [VOD Movies & Series](methods_vod.md) | Rubika streaming video: HLS playlists, filmography, watchlists, and search. | 9 methods |
| [Wallet & Payments](methods_wallet.md) | In-app credit, transaction history, balance queries, and user-to-user transfers. | 4 methods |
| [Universal Invoker](methods_invoker.md) | Execute any of the **301 reverse-engineered RPC methods** directly with custom payloads. | 301 methods |

---

## Standard Response Format

RubiFlow returns either typed model instances (such as `Message`, `Chat`, or `User`) or dictionary responses mirroring the server JSON. 

When invoking lower-level methods, the response dictionary follows this structure:

```json
{
  "status": "OK",
  "status_code": 200,
  "data": {
    "message_id": "1234567890",
    "chat_guid": "u0ABCDEF1234567890"
  }
}
```

If an error occurs, RubiFlow raises `RubikaRPCError` or `RubikaNetworkError` containing the server error code (e.g., `ERROR_GENERIC`, `TOO_MANY_REQUESTS`, `ACCESS_DENIED`).
"""

# ==============================================================================
# 2. Messaging & Polls (docs/methods_messages.md)
# ==============================================================================
methods_messages_md = """# 💬 Messaging & Polls API

Methods for sending, editing, deleting, forwarding messages, managing pins, creating polls, and broadcasting chat actions.

---

### `send_message`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Use this method to send a text message to any user, group, or channel. On success, the sent [`Message`](#message-object) is returned.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | Target GUID of the user (`u...`), group (`g...`), or channel (`c...`). |
| `text` | `str` | Yes | Text of the message to be sent (1-4096 characters). |
| `reply_to_message_id` | `str` | No | Identifier of the target message to reply to. |

#### Code Example
```python
message = await app.send_message(
    target="u0ABCDEF123456789",
    text="Hello from RubiFlow! 🚀",
    reply_to_message_id="987654321"
)
print(f"Sent message ID: {message.message_id}")
```

---

### `forward_messages`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Use this method to forward messages of any kind. Service messages cannot be forwarded.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `from_chat` | `str` | Yes | Unique identifier for the origin chat GUID. |
| `to_chat` | `str` | Yes | Unique identifier for the target chat GUID. |
| `message_ids` | `List[str \| int]` | Yes | List of message IDs to forward. |

#### Code Example
```python
result = await app.forward_messages(
    from_chat="c0ABCDEF...",
    to_chat="g0ABCDEF...",
    message_ids=["1001", "1002"]
)
```

---

### `edit_message_text`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Use this method to edit text and game messages.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | Chat GUID where the message was sent. |
| `message_id` | `str \| int` | Yes | Identifier of the message to edit. |
| `new_text` | `str` | Yes | New text of the message. |

#### Code Example
```python
await app.edit_message_text(
    target="u0ABCDEF...",
    message_id="1001",
    new_text="This message has been updated with new information."
)
```

---

### `delete_messages`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Use this method to delete one or more messages in a chat.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | Target chat GUID. |
| `message_ids` | `List[str \| int]` | Yes | List of message IDs to delete. |
| `delete_for_all` | `bool` | No | Pass `True` to delete for all members in group/channel. Defaults to `True`. |

#### Code Example
```python
await app.delete_messages(
    target="g0ABCDEF...",
    message_ids=["1001", "1002"],
    delete_for_all=True
)
```

---

### `get_messages_interval`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Retrieves a window of messages around a given message ID.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | Target chat GUID. |
| `middle_message_id` | `str \| int` | Yes | The anchor message ID around which surrounding messages will be fetched. |

#### Return Value
Returns a list of [`Message`](#message-object) objects.

#### Code Example
```python
messages = await app.get_messages_interval(target="c0ABCDEF...", middle_message_id="500")
for msg in messages:
    print(f"[{msg.message_id}] {msg.author_guid}: {msg.text}")
```

---

### `pin_chat_message`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Pins a message at the top of a group or channel.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | Target chat GUID. |
| `message_id` | `str \| int` | Yes | Identifier of a message to pin. |
| `notify_members` | `bool` | No | Pass `True` if it is not necessary to send a notification to all chat members. Defaults to `True`. |

---

### `unpin_chat_message`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Removes a pinned message from a group or channel.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | Target chat GUID. |
| `message_id` | `str \| int` | Yes | Identifier of a message to unpin. |

---

### `create_poll`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Creates and sends an interactive native poll in a chat.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | Target chat GUID. |
| `question` | `str` | Yes | Poll question, 1-300 characters. |
| `options` | `List[str]` | Yes | A list of 2-10 answer options. |
| `is_anonymous` | `bool` | No | `True` if the poll needs to be anonymous. Defaults to `True`. |
| `allows_multiple_answers` | `bool` | No | `True` if the poll allows multiple answers. Defaults to `False`. |

#### Code Example
```python
poll_msg = await app.create_poll(
    target="g0ABCDEF...",
    question="What framework do you prefer for Rubika bots?",
    options=["RubiFlow", "rubika-py", "Manual Requests"],
    is_anonymous=False
)
```

---

### `vote_poll`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Votes on an existing poll.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | Target chat GUID. |
| `poll_id` | `str` | Yes | Unique poll identifier. |
| `selection_index` | `int` | Yes | 0-indexed choice option. |

---

### `send_chat_activity`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Broadcasts typing or uploading activity to a chat. The status is set for 5 seconds or until the next message arrives.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | Target chat GUID. |
| `activity` | `str` | No | Type of action: `'Typing'`, `'Uploading'`, `'RecordingAudio'`. Defaults to `'Typing'`. |

#### Code Example
```python
await app.send_chat_activity("u0ABCDEF...", activity="Typing")
```

---

### `search_chat_messages` / `search_global_messages`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Searches for text within a single chat or across all joined chats.

#### Code Example
```python
# Search inside a specific chat
results = await app.search_chat_messages("c0ABCDEF...", search_text="python")

# Search across all conversations
global_results = await app.search_global_messages("announcement")
```
"""

# ==============================================================================
# 3. Chats & Dialogs (docs/methods_chats.md)
# ==============================================================================
methods_chats_md = """# 💬 Chats & Dialogs API

Methods for managing dialog lists, unread counters, reading status, and conversation history.

---

### `get_chats`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Use this method to fetch a user's recent conversations and dialogs with pagination support.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `start_id` | `str` | No | Cursor identifier for pagination (offset). Defaults to `None`. |
| `limit` | `int` | No | Maximum number of dialogs to fetch (default `50`). |

#### Return Value
Returns a list of [`Chat`](#chat-object) objects.

#### Code Example
```python
chats = await app.get_chats(limit=30)
for chat in chats:
    print(f"Title: {chat.title} | GUID: {chat.guid} | Unread: {chat.count_unseen}")
```

---

### `get_chat`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Fetches detailed metadata about a single conversation.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | Target chat GUID (`u...`, `g...`, `c...`). |

#### Code Example
```python
chat = await app.get_chat("g0ABCDEF123456789")
print(f"Chat Title: {chat.title}")
print(f"Pinned Message: {chat.pinned_message_id}")
```

---

### `seen_chats`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Marks messages up to a given message ID as read (seen) across multiple chats.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `seen_map` | `Dict[str, int]` | Yes | Mapping of `{chat_guid: last_seen_message_id}`. |

#### Code Example
```python
await app.seen_chats({
    "u0ABCDEF...": 1520,
    "c0BCDEF...": 890
})
```

---

### `delete_chat_history`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Deletes all message history within a private conversation.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | Target user chat GUID (`u...`). |

---

### `search_chats`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Searches the user's active dialog list by chat title or member name.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `search_text` | `str` | Yes | Query string. |

#### Code Example
```python
matching_chats = await app.search_chats("Developers")
for chat in matching_chats:
    print(f"Found: {chat.title} ({chat.guid})")
```
"""

# ==============================================================================
# 4. Groups & Voice Chats (docs/methods_groups.md)
# ==============================================================================
methods_groups_md = """# 👥 Groups & Voice Chats API

Methods for managing supergroups, member administration, permission control, and WebRTC voice chats.

---

### `create_group`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Creates a new supergroup chat.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `title` | `str` | Yes | Name of the group (1-255 characters). |
| `member_guids` | `List[str]` | No | Initial list of user GUIDs to add to the group. |

#### Code Example
```python
result = await app.create_group(
    title="RubiFlow Developers Group",
    member_guids=["u0ABCDEF12345"]
)
group_guid = result["group"]["group_guid"]
print(f"New Group Created: {group_guid}")
```

---

### `get_group_info`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Retrieves full group metadata including member count, description, invite link, and avatar.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `group_guid` | `str` | Yes | Group GUID (`g...`). |

#### Code Example
```python
info = await app.get_group_info("g0ABCDEF12345")
print(f"Group: {info['group']['group_title']}")
print(f"Members: {info['group']['count_members']}")
print(f"Description: {info['group']['description']}")
```

---

### `add_group_members`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Adds one or more users to a group.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `group_guid` | `str` | Yes | Target group GUID. |
| `member_guids` | `List[str]` | Yes | List of user GUIDs to add. |

---

### `ban_group_member`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Removes and kicks a user from a group.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `group_guid` | `str` | Yes | Target group GUID. |
| `member_guid` | `str` | Yes | User GUID to ban/kick. |

---

### `set_group_admin`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Promotes a user to an administrator with specific fine-grained privileges, or demotes them.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `group_guid` | `str` | Yes | Target group GUID. |
| `member_guid` | `str` | Yes | User GUID to promote or demote. |
| `access_list` | `List[str]` | Yes | List of granted permissions: `['ChangeInfo', 'PinMessages', 'DeleteMessages', 'BanMember', 'SetAdmin']`. |
| `action` | `str` | No | `'SetAdmin'` or `'UnsetAdmin'`. Defaults to `'SetAdmin'`. |

#### Code Example
```python
await app.set_group_admin(
    group_guid="g0ABCDEF...",
    member_guid="u0ABCDEF...",
    access_list=["DeleteMessages", "PinMessages"],
    action="SetAdmin"
)
```

---

### `set_group_default_access`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Sets default permissions for all regular members in a group (e.g. restrict sending media or messages).

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `group_guid` | `str` | Yes | Target group GUID. |
| `default_access` | `List[str]` | Yes | Allowed permissions for standard members: `['SendMessages', 'SendMedia']`. |

---

### Voice Chat Controls (WebRTC)
Rubika supports native audio voice chats in groups.

- **`create_group_voice_chat(group_guid, title=None)`**: Starts a new group voice chat room.
- **`join_group_voice_chat(group_guid, voice_chat_id, sdp_offer)`**: Submits a WebRTC SDP offer to join audio.
- **`discard_group_voice_chat(group_guid, voice_chat_id)`**: Ends and closes the voice chat room.
"""

# ==============================================================================
# 5. Channels & Broadcasts (docs/methods_channels.md)
# ==============================================================================
methods_channels_md = """# 📢 Channels & Broadcasts API

Methods for broadcasting content, managing channel subscribers, public handles, and administrators.

---

### `create_channel`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Creates a new broadcast channel.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `title` | `str` | Yes | Channel title. |
| `description` | `str` | No | Channel bio / description. |

#### Code Example
```python
res = await app.create_channel(
    title="RubiFlow News",
    description="Official channel for updates and announcements."
)
channel_guid = res["channel"]["channel_guid"]
print(f"Created Channel: {channel_guid}")
```

---

### `get_channel_info`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Retrieves channel information including subscriber count, username, and invite link.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `channel_guid` | `str` | Yes | Channel GUID (`c...`). |

---

### `update_channel_username`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Sets or updates the public `@username` for a broadcast channel.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `channel_guid` | `str` | Yes | Target channel GUID. |
| `username` | `str` | Yes | New username without `@` (e.g. `'rubiflow_official'`). |

---

### `join_channel_by_link` / `leave_channel`
<span class="badge post">POST</span> <span class="badge async">Async</span>

- **`join_channel_by_link(invite_link: str)`**: Subscribes to a private or public channel via invite link.
- **`leave_channel(channel_guid: str)`**: Leaves and unsubscribes from a channel.

---

### `get_channel_all_members` / `get_channel_admin_members`
<span class="badge post">POST</span> <span class="badge async">Async</span>

- **`get_channel_admin_members(channel_guid: str)`**: Lists all administrators and their permission grants.
- **`get_channel_all_members(channel_guid: str, search_text=None, start_id=None)`**: Lists channel subscribers with search support.
"""

# ==============================================================================
# 6. Users & Contacts (docs/methods_users.md)
# ==============================================================================
methods_users_md = """# 👤 Users & Contacts API

Methods for querying user profiles, blocking/unblocking accounts, managing address books, and reserving usernames.

---

### `get_me`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Returns basic information about the currently authenticated user.

#### Return Value
Returns a [`User`](#user-object) object.

#### Code Example
```python
me = await app.get_me()
print(f"Hello, {me.first_name} (@{me.username})! GUID: {me.guid}")
```

---

### `get_user_info`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Fetches a user profile, online status, bio, and avatar by their user GUID.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `user_guid` | `str` | Yes | Target user GUID (`u...`). |

#### Return Value
Returns a [`User`](#user-object) object.

#### Code Example
```python
user = await app.get_user_info("u0ABCDEF123456789")
print(f"User: {user.first_name} {user.last_name}")
print(f"Bio: {user.bio}")
print(f"Online: {user.is_online}")
```

---

### `update_profile`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Updates the user's first name, last name, or bio.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `first_name` | `str` | No | New first name. |
| `last_name` | `str` | No | New last name. |
| `bio` | `str` | No | New bio description (up to 70 characters). |

---

### `update_username` / `check_username`
<span class="badge post">POST</span> <span class="badge async">Async</span>

- **`check_username(username: str)`**: Checks if a handle is available on Rubika.
- **`update_username(username: str)`**: Reserves and claims the handle for the authenticated account.

---

### `block_user` / `unblock_user` / `get_blocked_users`
<span class="badge post">POST</span> <span class="badge async">Async</span>

- **`block_user(user_guid: str)`**: Blocks incoming messages and calls from a user.
- **`unblock_user(user_guid: str)`**: Unblocks a previously blocked user.
- **`get_blocked_users()`**: Lists all blocked contacts.

---

### Address Book Synchronization
- **`get_contacts()`**: Retrieves synced phone contacts.
- **`add_address_book(first_name, last_name, phone)`**: Adds a new contact by phone number.
- **`delete_contact(user_guid)`**: Deletes a contact from the address book.
"""

# ==============================================================================
# 7. Cloud Files & CDN (docs/methods_files.md)
# ==============================================================================
methods_files_md = """# 📁 Cloud Files & CDN API

RubiFlow handles high-speed chunked uploading and downloading across Rubika's distributed media CDN clusters.

---

### `upload_file`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Uploads a local file or raw bytes to Rubika CDN nodes and returns file metadata ready to be attached to messages or posts.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `file_input` | `str \| bytes` | Yes | Local file path (`str`) or raw file contents in memory (`bytes`). |
| `file_name` | `str` | No | Explicit file name. If omitted, extracted from path. |
| `mime` | `str` | No | MIME type of the file. Defaults to `'application/octet-stream'`. |

#### Return Value
```python
{
    "file_id": "1234567890",
    "access_hash_send": "9876543210...",
    "mime": "image/jpeg",
    "size": 1048576,
    "file_name": "photo.jpg"
}
```

#### Code Example
```python
file_meta = await app.upload_file("wallpaper.jpg", mime="image/jpeg")
print(f"Uploaded File ID: {file_meta['file_id']}")
```

---

### `download_file`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Downloads a file from Rubika CDN using its `file_id` and `access_hash_rec`.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `file_id` | `str \| int` | Yes | File identifier. |
| `access_hash_rec` | `str` | Yes | Received access hash for the file. |
| `save_path` | `str` | No | Local destination file path. If `None`, returns raw `bytes`. |

#### Code Example
```python
# Download to disk
await app.download_file(file_id="12345", access_hash_rec="hash...", save_path="downloaded.png")

# Download to memory
data_bytes = await app.download_file(file_id="12345", access_hash_rec="hash...")
```

---

### Stickers
- **`get_trend_sticker_sets()`**: Retrieves list of trending sticker packs.
- **`get_my_sticker_sets()`**: Lists user's saved sticker collections.
"""

# ==============================================================================
# 8. Folders & Organization (docs/methods_folders.md)
# ==============================================================================
methods_folders_md = """# 🗂️ Folders & Organization API

Rubika supports chat categorization through custom folders (tabs) like Telegram.

---

### `get_folders`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Retrieves all configured chat folders for the account.

```python
folders = await app.get_folders()
for folder in folders:
    print(f"Folder: {folder['name']} | ID: {folder['folder_id']}")
```

---

### `create_folder`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Creates a new custom chat tab.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | Yes | Folder tab title (e.g. `'Work'`, `'Bots'`). |
| `include_chat_types` | `List[str]` | Yes | Chat categories to include: `['Users', 'Groups', 'Channels', 'Bots']`. |
| `exclude_chat_types` | `List[str]` | No | Optional chat categories to exclude. |

#### Code Example
```python
await app.create_folder(
    name="Channels",
    include_chat_types=["Channels"]
)
```

---

### `delete_folder`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Deletes a chat folder by its ID.
"""

# ==============================================================================
# 9. Settings & Privacy (docs/methods_settings.md)
# ==============================================================================
methods_settings_md = """# ⚙️ Settings & Privacy API

Manage account security, two-step verification, appearance themes, and active login sessions.

---

### Two-Step Verification (2FA)
- **`setup_two_step_verification(password, hint=None, recovery_email=None)`**: Sets a master password for login.
- **`set_recovery_email(email)`**: Configures a recovery email address.
- **`verify_recovery_email(email_code)`**: Confirms the email verification code.

---

### Privacy & Notifications
- **`get_privacy_settings()`** / **`set_privacy_setting(privacy_dict)`**: Configures who can see last seen status, phone number, and profile pictures (`Everybody`, `MyContacts`, `Nobody`).
- **`get_notification_settings()`** / **`set_notification_setting(notification_dict)`**: Controls sound, preview, and vibration.
- **`get_appearance_settings()`** / **`set_appearance_setting(setting_dict)`**: Controls theme (Dark, Light) and text scaling.

---

### Active Sessions Management
- **`terminate_session(session_key: str)`**: Terminates a specific device login.
- **`terminate_user_sessions()`**: Logs out all other active sessions except the current one.
"""

# ==============================================================================
# 10. Rubino Social Network (docs/methods_rubino.md)
# ==============================================================================
methods_rubino_md = """# 📸 Rubino Social Network API

Rubino is Rubika's built-in Instagram-style social platform. RubiFlow provides complete access to Rubino creators, explore feeds, likes, comments, and stories.

---

### `get_rubino_explore`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Fetches the infinite-scroll Explore feed.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `limit` | `int` | No | Number of posts to retrieve (default `24`). |
| `max_id` | `str` | No | Pagination cursor. |

#### Code Example
```python
explore = await app.get_rubino_explore(limit=10)
for post in explore.get("posts", []):
    print(f"Post {post['id']} by @{post['profile']['username']}: {post.get('caption')}")
```

---

### `get_rubino_profile_info` / `get_rubino_profile_posts`
<span class="badge post">POST</span> <span class="badge async">Async</span>

- **`get_rubino_profile_info(profile_id: str)`**: Gets follower count, bio, and profile details.
- **`get_rubino_profile_posts(profile_id: str, limit=20, max_id=None)`**: Retrieves a creator's published grid posts.

---

### Interacting with Posts
- **`like_post(post_id: str, profile_id: str)`**: Likes a Rubino post.
- **`unlike_post(post_id: str, profile_id: str)`**: Unlikes a post.
- **`bookmark_post(post_id: str, profile_id: str)`**: Saves a post to bookmarks.
- **`unbookmark_post(post_id: str, profile_id: str)`**: Removes a post from bookmarks.

---

### Comments & Discussions
- **`add_comment(post_id: str, profile_id: str, content: str)`**: Posts a comment on a photo or video.
- **`like_comment(comment_id: str, post_id: str, profile_id: str)`**: Likes a comment.
- **`get_comments(post_id: str, profile_id: str, limit=20)`**: Lists comments on a post.

---

### Social Graph & Following
- **`request_follow(target_profile_id: str, action='Follow')`**: Follows or unfollows a creator profile (`'Follow'` or `'Unfollow'`).
- **`get_story(story_id: str, profile_id: str)`**: Fetches story media and viewer counts.
- **`get_story_viewers(story_id: str, profile_id: str)`**: Retrieves list of users who watched a story.

---

### Search
- **`search_rubino_profile(search_text: str)`**: Finds creators by name or username.
- **`search_rubino_hashtag(search_text: str)`**: Searches posts by hashtag.
"""

# ==============================================================================
# 11. VOD Movies & Series (docs/methods_vod.md)
# ==============================================================================
methods_vod_md = """# 🎬 VOD Movies & Series API

Access Rubika's streaming media platform: movies, TV series, HLS streaming playlists, and cast filmography.

---

### `search_vod`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Searches the Rubika VOD entertainment catalog.

```python
results = await app.search_vod("Inception")
for movie in results:
    print(f"Title: {movie['title']} | ID: {movie['id']}")
```

---

### `get_vod_media` / `get_vod_play_info`
<span class="badge post">POST</span> <span class="badge async">Async</span>

- **`get_vod_media(media_id: str)`**: Fetches synopsis, genres, duration, and cover art.
- **`get_vod_play_info(media_id: str)`**: Returns HLS video stream playlist URLs (`.m3u8`) and playback tokens.

---

### TV Series & Episodes
- **`get_vod_season_episodes(series_id: str, season_id=None)`**: Lists episodes of a TV show with streaming links.

---

### Watchlist & Progress
- **`get_vod_wishlist()`**: Lists user's saved movies and shows.
- **`add_vod_wishlist(media_id: str)`**: Adds a title to watchlist.
- **`set_vod_play_time(media_id: str, play_time_seconds: int)`**: Synchronizes resume playback position across devices.
"""

# ==============================================================================
# 12. Wallet & Payments (docs/methods_wallet.md)
# ==============================================================================
methods_wallet_md = """# 💳 Wallet & Payments API

Methods for querying in-app balance, checking transaction logs, and transferring credit between users.

---

### `get_wallet_status`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Returns the user's current digital wallet balance and currency codes.

```python
status = await app.get_wallet_status()
print(f"Available Balance: {status.get('balance')} Rials")
```

---

### `get_wallet_transactions`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Fetches recent transaction history with timestamps, amounts, and statuses.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `limit` | `int` | No | Number of transactions (default `20`). |

---

### `transfer_credit`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Transfers balance directly to another Rubika user.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `recipient_guid` | `str` | Yes | Target user GUID (`u...`). |
| `amount` | `int` | Yes | Amount in Rials. |
"""

# ==============================================================================
# 13. Direct Invoker (docs/methods_invoker.md)
# ==============================================================================
methods_invoker_md = """# ⚡ Direct RPC Invoker (`app.invoke`)

While RubiFlow provides high-level typed helper methods for common operations, it also provides a direct low-level invoker capable of executing **any of the 301 reverse-engineered RPC methods** with arbitrary payloads.

---

### Syntax

```python
result = await app.invoke(method_name: str, **kwargs)
```

The invoker automatically:
1. Wraps your arguments into the required Rubika RPC envelope.
2. Resolves the correct API endpoint (Messenger, Rubino, or VOD).
3. Generates the 32-character AES key and encrypts the payload using AES-256-CBC.
4. Encodes and disguises the authentication token using the `em` substitution cipher.
5. Signs the request using RSA-SHA256 (if temporary key is active).
6. Decrypts and unpacks the JSON response from the server.

---

### Example: Invoking any Raw Method

```python
from rubiflow import Client

app = Client.from_firefox()

async def main():
    async with app:
        # Call raw 'getUserInfo'
        user_raw = await app.invoke("getUserInfo", user_guid="u0ABCDEF...")
        print(user_raw)

        # Call raw Rubino method
        explore_raw = await app.invoke("getExplorePosts", limit=10)
        print(explore_raw)

if __name__ == "__main__":
    app.run(main())
```

---

### Full Catalog of 301 Supported Methods

Refer to the complete reverse-engineered catalog:
- 👉 [All 301 Methods Catalog](RUBIKA_API_FULL_REFERENCE.md)
"""

# ==============================================================================
# 14. Bot API & Event Handlers (docs/bot_api.md)
# ==============================================================================
bot_api_md = """# 🤖 Bot API & Event-Driven Engine

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
        await msg.reply("Welcome to RubiFlow Bot! 🚀\\nSend me any text and I will echo it.")
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
        chat_info = f"Chat GUID: `{msg.chat_guid}`\\nMessage ID: `{msg.message_id}`"
        await msg.reply(chat_info)

    elif text.startswith("/help"):
        await msg.reply(
            "Available commands:\\n"
            "/info - Show chat ID\\n"
            "/ping - Check bot response\\n"
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
"""

# ==============================================================================
# 15. Cryptography & V6 Protocol (docs/cryptography.md)
# ==============================================================================
cryptography_md = """# 🔐 Rubika V6 Cryptography & Security

RubiFlow implements the full **Rubika V6 Protocol**, reverse-engineered from the official Web and PWA clients (`web.rubika.ir` and `m.rubika.ir`).

---

## 1. Key Derivation (`create_secret_passphrase`)

Rubika requires an ephemeral 32-character AES secret key derived from the user's permanent authentication token:

```
Passphrase = Token[0:8] + Token[16:24] + Token[8:16] + Token[24:32]
```

### Python Implementation:
```python
def create_secret_passphrase(auth_token: str) -> str:
    if len(auth_token) < 32:
        auth_token = auth_token.ljust(32, "a")
    return (
        auth_token[0:8]
        + auth_token[16:24]
        + auth_token[8:16]
        + auth_token[24:32]
    )
```

---

## 2. AES-256-CBC Payload Encryption

Every RPC request payload is serialized to JSON, padded with standard PKCS#7 padding, and encrypted using AES-256-CBC:
- **Cipher:** `AES-256-CBC`
- **Key:** Derived 32-byte secret passphrase (`utf-8` encoded).
- **IV:** 16 zero bytes (`b'\\x00' * 16`).
- **Encoding:** Base64.

---

## 3. Token Disguise (`disguise_auth` / `em` Cipher)

Rubika passes the authentication token in request headers using a custom character substitution table:

| Plain | Disguised | Plain | Disguised |
| :---: | :---: | :---: | :---: |
| `a` | `g` | `0` | `y` |
| `b` | `h` | `1` | `z` |
| `c` | `i` | `2` | `0` |
| `d` | `j` | `3` | `1` |
| `e` | `k` | `4` | `2` |
| `...` | `...` | `9` | `7` |

RubiFlow handles this translation bidirectionally automatically.

---

## 4. Client Handshake Identification

Rubika validates the inner client header inside the encrypted envelope. Non-standard identifiers are rejected by the server with `ERROR_GENERIC`.

RubiFlow uses the exact compliant descriptor:
```json
{
  "app_name": "Main",
  "app_version": "2.5.9",
  "platform": "PWA",
  "package": "m.rubika.ir",
  "lang_code": "fa"
}
```

Device branding (such as `"RubiFlow Framework"`) is registered via the server's dedicated `registerDevice` RPC method without triggering signature checks.
"""

# Write all documents
docs_to_generate = {
    "api_reference.md": api_reference_md,
    "methods_messages.md": methods_messages_md,
    "methods_chats.md": methods_chats_md,
    "methods_groups.md": methods_groups_md,
    "methods_channels.md": methods_channels_md,
    "methods_users.md": methods_users_md,
    "methods_files.md": methods_files_md,
    "methods_folders.md": methods_folders_md,
    "methods_settings.md": methods_settings_md,
    "methods_rubino.md": methods_rubino_md,
    "methods_vod.md": methods_vod_md,
    "methods_wallet.md": methods_wallet_md,
    "methods_invoker.md": methods_invoker_md,
    "bot_api.md": bot_api_md,
    "cryptography.md": cryptography_md,
}

for filename, content in docs_to_generate.items():
    write_doc(filename, content)

print("All documentation pages generated successfully!")
