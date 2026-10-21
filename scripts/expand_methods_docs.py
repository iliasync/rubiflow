"""
Expands channels, groups, files, chats, and users documentation pages
with comprehensive parameters tables, return models, and code samples.
"""

import os

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))

def save_doc(filename: str, content: str):
    path = os.path.join(DOCS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Expanded: {filename} ({len(content.splitlines())} lines)")

# ==============================================================================
# methods_channels.md
# ==============================================================================
methods_channels_md = """# 📢 Channels & Broadcasts API

Comprehensive reference for creating broadcast channels, managing subscribers, administering permissions, and reserving channel usernames.

---

### `create_channel`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Creates a new broadcast channel where only administrators can post messages.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `title` | `str` | Yes | - | Channel name (1-255 characters). |
| `description` | `str` | No | `""` | Optional channel biography/description. |

#### Return Value
Returns a dictionary containing the created channel object:
```json
{
  "status": "OK",
  "data": {
    "channel": {
      "channel_guid": "c0ABCDEF1234567890",
      "channel_title": "RubiFlow News",
      "count_members": 1
    }
  }
}
```

#### Code Example
```python
res = await app.create_channel(
    title="RubiFlow Announcements",
    description="Official channel for updates, releases, and guides."
)
channel_guid = res["channel"]["channel_guid"]
print(f"Created channel: {channel_guid}")
```

---

### `get_channel_info`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Retrieves channel information including subscriber count, description, invite link, and avatar.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `channel_guid` | `str` | Yes | - | Target channel GUID (`c0...`). |

#### Return Value
```json
{
  "status": "OK",
  "data": {
    "channel": {
      "channel_guid": "c0ABCDEF...",
      "channel_title": "My Channel",
      "count_members": 2500,
      "description": "Welcome to our channel!",
      "share_url": "https://rubika.ir/joinc/...",
      "username": "my_channel_handle"
    }
  }
}
```

#### Code Example
```python
info = await app.get_channel_info("c0ABCDEF12345")
print(f"Subscribers: {info['channel']['count_members']}")
print(f"Invite Link: {info['channel']['share_url']}")
```

---

### `add_channel_members`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Adds one or more users to a channel as subscribers.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `channel_guid` | `str` | Yes | - | Target channel GUID. |
| `member_guids` | `List[str]` | Yes | - | List of user GUIDs to subscribe. |

#### Code Example
```python
await app.add_channel_members(
    channel_guid="c0ABCDEF...",
    member_guids=["u0User1...", "u0User2..."]
)
```

---

### `update_channel_username`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Sets or updates the public `@username` for a broadcast channel.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `channel_guid` | `str` | Yes | - | Target channel GUID. |
| `username` | `str` | Yes | - | Desired public handle without `@` (e.g. `'my_brand'`). |

---

### `join_channel_by_link`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Subscribes the authenticated account to a channel using its public or private invite link.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `invite_link` | `str` | Yes | - | Full invite link (e.g. `'https://rubika.ir/joinc/ABCDEF'`). |

#### Code Example
```python
await app.join_channel_by_link("https://rubika.ir/joinc/ABCDEF123456")
```

---

### `leave_channel`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Leaves and unsubscribes from a channel.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `channel_guid` | `str` | Yes | - | Channel GUID to leave. |

---

### `set_channel_admin`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Promotes a subscriber to channel administrator with specific permissions, or demotes them.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `channel_guid` | `str` | Yes | - | Target channel GUID. |
| `member_guid` | `str` | Yes | - | User GUID to promote or demote. |
| `access_list` | `List[str]` | Yes | - | Granted permissions: `['ChangeInfo', 'PostMessages', 'EditMessages', 'DeleteMessages', 'AddMember', 'SetAdmin']`. |
| `action` | `str` | No | `'SetAdmin'` | `'SetAdmin'` to grant, or `'UnsetAdmin'` to revoke. |

#### Code Example
```python
await app.set_channel_admin(
    channel_guid="c0ABCDEF...",
    member_guid="u0TargetUser...",
    access_list=["PostMessages", "EditMessages", "DeleteMessages"],
    action="SetAdmin"
)
```

---

### `get_channel_admin_members`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Retrieves a list of all administrators and creator details in the channel.

---

### `get_channel_all_members`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Lists channel subscribers with search and pagination support.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `channel_guid` | `str` | Yes | - | Target channel GUID. |
| `search_text` | `str` | No | `None` | Query filter for subscriber name. |
| `start_id` | `str` | No | `None` | Pagination cursor offset. |
"""

# ==============================================================================
# methods_groups.md
# ==============================================================================
methods_groups_md = """# 👥 Groups & Voice Chats API

Comprehensive reference for managing supergroups, member administration, permission moderation, and WebRTC voice chats.

---

### `create_group`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Creates a new group conversation.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `title` | `str` | Yes | - | Group name (1-255 characters). |
| `member_guids` | `List[str]` | No | `None` | Initial list of user GUIDs to invite into the group. |

#### Return Value
```json
{
  "status": "OK",
  "data": {
    "group": {
      "group_guid": "g0ABCDEF1234567890",
      "group_title": "RubiFlow Developers",
      "count_members": 2
    }
  }
}
```

#### Code Example
```python
res = await app.create_group(
    title="RubiFlow Community",
    member_guids=["u0ABCDEF12345"]
)
group_guid = res["group"]["group_guid"]
print("Created group:", group_guid)
```

---

### `get_group_info`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Retrieves full metadata for a group, including member count, description, invite link, and avatar.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `group_guid` | `str` | Yes | - | Target group GUID (`g0...`). |

---

### `add_group_members`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Adds one or more users to a group.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `group_guid` | `str` | Yes | - | Target group GUID. |
| `member_guids` | `List[str]` | Yes | - | List of user GUIDs to add. |

---

### `ban_group_member`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Kicks and bans a user from a group.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `group_guid` | `str` | Yes | - | Target group GUID. |
| `member_guid` | `str` | Yes | - | User GUID to ban. |

#### Code Example
```python
# Kick a spammer
await app.ban_group_member("g0ABCDEF...", "u0SpammerGUID...")
```

---

### `set_group_admin`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Promotes a member to administrator with granular permissions, or revokes admin status.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `group_guid` | `str` | Yes | - | Target group GUID. |
| `member_guid` | `str` | Yes | - | Target user GUID. |
| `access_list` | `List[str]` | Yes | - | Privileges: `['ChangeInfo', 'PinMessages', 'DeleteMessages', 'BanMember', 'SetAdmin']`. |
| `action` | `str` | No | `'SetAdmin'` | `'SetAdmin'` or `'UnsetAdmin'`. |

---

### `set_group_default_access`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Configures default permissions for all regular group members (e.g. lock group from sending messages or media).

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `group_guid` | `str` | Yes | - | Target group GUID. |
| `default_access` | `List[str]` | Yes | - | Allowed actions: `['SendMessages', 'SendMedia']`. |

#### Code Example
```python
# Mute group for regular members (night mode)
await app.set_group_default_access(
    group_guid="g0ABCDEF...",
    default_access=[]
)
```

---

### `edit_group_info`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Updates group title or bio/description.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `group_guid` | `str` | Yes | - | Target group GUID. |
| `title` | `str` | No | `None` | New group title. |
| `description` | `str` | No | `None` | New group description. |

---

### `leave_group`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Leaves and exits a group.

---

### WebRTC Voice Chats

- **`create_group_voice_chat(group_guid: str, title: Optional[str] = None)`**: Starts an interactive group audio voice chat room.
- **`join_group_voice_chat(group_guid: str, voice_chat_id: str, sdp_offer: str)`**: Submits a WebRTC SDP offer to connect audio streams.
- **`discard_group_voice_chat(group_guid: str, voice_chat_id: str)`**: Ends and closes the voice chat room.
"""

# ==============================================================================
# methods_files.md
# ==============================================================================
methods_files_md = """# 📁 Cloud Files, CDN & Stickers API

RubiFlow handles high-speed uploading and downloading across Rubika's distributed media CDN storage clusters.

---

### `upload_file`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Uploads a local file or in-memory byte buffer to Rubika CDN nodes and returns file metadata ready to be attached to messages or posts.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `file_input` | `Union[str, bytes]` | Yes | - | File path on disk (`str`) or raw file bytes in memory (`bytes`). |
| `file_name` | `str` | No | `None` | Custom file name. If omitted, derived from path or generated. |
| `mime` | `str` | No | `'application/octet-stream'` | MIME type (e.g. `'image/jpeg'`, `'video/mp4'`). |

#### Return Value
Returns a file metadata dictionary:
```json
{
  "file_id": "1049285712",
  "access_hash_send": "349102847501928471029384",
  "mime": "image/png",
  "size": 492048,
  "file_name": "screenshot.png",
  "cdn_url": "https://storage.iranlms.ir/..."
}
```

#### Code Example
```python
# Upload from disk path
meta = await app.upload_file("charts/report.pdf", mime="application/pdf")
print(f"Uploaded file ID: {meta['file_id']}")

# Upload in-memory bytes
import io
bio = io.BytesIO(b"Hello Rubika Cloud File")
meta2 = await app.upload_file(bio.getvalue(), file_name="memo.txt", mime="text/plain")
```

---

### `download_file`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Downloads a media file or document from Rubika CDN nodes.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `file_id` | `Union[str, int]` | Yes | - | Unique file identifier. |
| `access_hash_rec` | `str` | Yes | - | Received access hash for the file. |
| `save_path` | `str` | No | `None` | Local destination file path. If `None`, returns raw `bytes`. |

#### Code Example
```python
# Download and save to disk
await app.download_file(
    file_id="1049285712",
    access_hash_rec="349102847501928471029384",
    save_path="downloads/photo.jpg"
)

# Download into memory as bytes
file_bytes = await app.download_file(
    file_id="1049285712",
    access_hash_rec="349102847501928471029384"
)
print("Downloaded size:", len(file_bytes), "bytes")
```

---

### `request_send_file`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Low-level method to request an upload token and assigned storage CDN endpoint for a file before streaming chunks.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `file_name` | `str` | Yes | - | File name. |
| `size` | `int` | Yes | - | Size of the file in bytes. |
| `mime` | `str` | Yes | - | MIME type. |

---

### Sticker Packs

- **`get_trend_sticker_sets() -> List[Dict[str, Any]]`**: Retrieves a list of trending and featured sticker sets.
- **`get_my_sticker_sets() -> List[Dict[str, Any]]`**: Lists the user's saved sticker pack collections.
"""

# ==============================================================================
# methods_users.md
# ==============================================================================
methods_users_md = """# 👤 Users & Contacts API

Methods for querying user profiles, blocking/unblocking accounts, managing address books, and reserving handles.

---

### `get_me`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Returns information about the currently authenticated account.

#### Return Value
Returns a [`User`](types.md#user) object.

#### Code Example
```python
me = await app.get_me()
print(f"Logged in as: {me.full_name} (@{me.username})")
print(f"User GUID   : {me.guid}")
print(f"Phone       : {me.phone}")
```

---

### `get_user_info`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Fetches a user profile, online presence, bio, and avatar by their user GUID.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `user_guid` | `str` | Yes | - | Target user GUID (`u0...`). |

#### Return Value
Returns a [`User`](types.md#user) object.

#### Code Example
```python
user = await app.get_user_info("u0ABCDEF123456789")
print(f"User: {user.full_name}")
print(f"Bio: {user.bio}")
print(f"Is Online: {user.is_online}")
```

---

### `update_profile`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Updates the user's first name, last name, or bio.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `first_name` | `str` | No | `None` | New first name. |
| `last_name` | `str` | No | `None` | New last name. |
| `bio` | `str` | No | `None` | New biography text (up to 70 characters). |

#### Code Example
```python
await app.update_profile(
    first_name="Mahan",
    bio="Building bots with RubiFlow ⚡"
)
```

---

### `check_username` / `update_username`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`check_username(username: str) -> Dict[str, Any]`**: Checks if an `@username` handle is available on Rubika.
- **`update_username(username: str) -> Dict[str, Any]`**: Reserves and claims the handle for the current account.

#### Code Example
```python
status = await app.check_username("my_cool_bot")
if status.get("data", {}).get("is_available"):
    await app.update_username("my_cool_bot")
    print("Username claimed!")
```

---

### `block_user` / `unblock_user` / `get_blocked_users`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`block_user(user_guid: str)`**: Blocks incoming messages and calls from a user.
- **`unblock_user(user_guid: str)`**: Unblocks a previously blocked user.
- **`get_blocked_users() -> List[Dict[str, Any]]`**: Retrieves the list of all blocked contacts.

---

### Address Book Contacts

- **`get_contacts() -> List[Dict[str, Any]]`**: Retrieves synced address book contacts.
- **`add_address_book(first_name: str, last_name: str, phone: str)`**: Adds a new contact by phone number.
- **`delete_contact(user_guid: str)`**: Removes a contact from the address book.
"""

# ==============================================================================
# methods_chats.md
# ==============================================================================
methods_chats_md = """# 💬 Chats & Dialogs API

Methods for managing conversations, retrieving dialog lists, marking chats as read, and deleting history.

---

### `get_chats`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Fetches recent conversations and dialogs with pagination support.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `start_id` | `str` | No | `None` | Cursor offset for pagination. |
| `limit` | `int` | No | `50` | Maximum number of dialogs to fetch (default `50`). |

#### Return Value
Returns a list of [`Chat`](types.md#chat) objects.

#### Code Example
```python
chats = await app.get_chats(limit=30)
for chat in chats:
    print(f"[{chat.chat_type}] {chat.title} (GUID: {chat.guid}) - Unread: {chat.count_unseen}")
```

---

### `get_chat`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Fetches detailed metadata about a single conversation.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | - | Target chat GUID (`u...`, `g...`, `c...`). |

#### Return Value
Returns a [`Chat`](types.md#chat) object.

---

### `seen_chats`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Marks messages up to a given message ID as read (seen) across one or multiple chats.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `seen_map` | `Dict[str, int]` | Yes | - | Mapping of `{chat_guid: last_seen_message_id}`. |

#### Code Example
```python
# Mark messages as read in user and channel
await app.seen_chats({
    "u0ABCDEF...": 1520,
    "c0BCDEF...": 890
})
```

---

### `search_chats`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Searches the user's active dialog list by chat title or member name.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `search_text` | `str` | Yes | - | Query string. |

---

### `delete_chat_history`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Deletes all message history within a private conversation.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `target` | `str` | Yes | - | Target user GUID (`u0...`). |
"""

expanded_docs = {
    "methods_channels.md": methods_channels_md,
    "methods_groups.md": methods_groups_md,
    "methods_files.md": methods_files_md,
    "methods_users.md": methods_users_md,
    "methods_chats.md": methods_chats_md,
}

for filename, content in expanded_docs.items():
    save_doc(filename, content)

print("Expanded all methods documentation successfully!")
