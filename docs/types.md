# 📦 Available Types & Data Models

This page describes all core data models, structures, and helper classes used throughout RubiFlow. All objects are strongly typed, dataclass-backed, and provide convenient serialization and manipulation helpers.

---

## `User`
Represents a Rubika user profile account.

### Fields
| Field | Type | Description |
| :--- | :--- | :--- |
| `guid` | `str` | Unique 32-character global identifier of the user (starts with `u0`). |
| `first_name` | `str` | First name of the user. |
| `last_name` | `Optional[str]` | Last name of the user, if set. |
| `username` | `Optional[str]` | Public handle without `@` symbol, if reserved. |
| `phone` | `Optional[str]` | Phone number in international format (only visible if allowed by privacy). |
| `bio` | `Optional[str]` | About text / biography (up to 70 characters). |
| `is_online` | `bool` | Whether the user is currently online on Rubika. |
| `last_online` | `Optional[int]` | Unix timestamp of when the user was last active. |
| `avatar_thumbnail` | `Optional[str]` | Base64-encoded micro thumbnail of avatar. |
| `raw` | `Dict[str, Any]` | Complete raw dictionary payload returned by the Rubika RPC server. |

### Properties
- `full_name` (`str`): Returns combined `"first_name last_name"`, stripping extra spaces.

#### Example
```python
user = await app.get_user_info("u0ABCDEF123456789")
print(f"Name: {user.full_name} (@{user.username})")
print(f"Online: {user.is_online}")
```

---

## `Chat`
Represents a conversation dialog (private chat, supergroup, or broadcast channel).

### Fields
| Field | Type | Description |
| :--- | :--- | :--- |
| `guid` | `str` | Unique GUID of the chat (`u...` for user, `g...` for group, `c...` for channel). |
| `title` | `str` | Title of the group, channel, or the contact's full name. |
| `chat_type` | `str` | Type identifier: `'User'`, `'Group'`, or `'Channel'`. |
| `count_unseen` | `int` | Number of unread messages waiting in this chat. |
| `last_message` | `Optional[Message]` | Most recent message received or sent in this dialog. |
| `pinned_message_id` | `Optional[str]` | Message ID of the currently pinned message, if any. |
| `time` | `int` | Unix timestamp of the last activity in the chat. |
| `raw` | `Dict[str, Any]` | Raw server response dictionary. |

### Properties
- `unread_count` (`int`): Alias for `count_unseen`.
- `is_user` (`bool`): `True` if `chat_type == 'User'`.
- `is_group` (`bool`): `True` if `chat_type == 'Group'`.
- `is_channel` (`bool`): `True` if `chat_type == 'Channel'`.

#### Example
```python
chats = await app.get_chats(limit=20)
for chat in chats:
    if chat.unread_count > 0:
        print(f"[{chat.chat_type}] {chat.title}: {chat.unread_count} unread messages")
```

---

## `Message`
Represents a message sent or received in any conversation.

### Fields
| Field | Type | Description |
| :--- | :--- | :--- |
| `message_id` | `str` | Unique identifier of the message inside the chat. |
| `chat_guid` | `str` | GUID of the chat (user, group, or channel) where message belongs. |
| `author_guid` | `str` | GUID of the user or channel that authored the message. |
| `text` | `str` | Text content of the message (empty string for media without caption). |
| `time` | `int` | Unix timestamp of when the message was sent. |
| `reply_to_message_id` | `Optional[str]` | Identifier of original message being replied to, if any. |
| `is_edited` | `bool` | `True` if message has been edited after transmission. |
| `raw` | `Dict[str, Any]` | Full raw message dictionary from Rubika. |

### Bound Async Methods
Every `Message` object received inside `@app.on_message()` or fetched via API has bound convenience methods:

#### `await msg.reply(text: str) -> Message`
Sends a reply quoting this exact message.
```python
@app.on_message()
async def handler(msg: Message):
    if msg.text == "/help":
        await msg.reply("Here is the help manual!")
```

#### `await msg.edit(new_text: str) -> Dict[str, Any]`
Edits the text of this message (if authored by self).
```python
sent = await app.send_message("u0...", "Processing...")
await asyncio.sleep(1)
await sent.edit("Finished processing!")
```

#### `await msg.delete(delete_for_all: bool = True) -> Dict[str, Any]`
Deletes this message.
```python
if "spam_word" in msg.text:
    await msg.delete()
```

#### `await msg.forward(to_chat: str) -> Dict[str, Any]`
Forwards this message to another chat GUID.
```python
await msg.forward("c0ArchiveChannelGUID...")
```

---

## `Session`
Represents the cryptographic identity and credentials of an authenticated Rubika session.

### Fields & Properties
| Attribute | Type | Description |
| :--- | :--- | :--- |
| `auth` | `str` | Permanent 32-character authentication token string. |
| `private_key_pem` | `str` | RSA private key in standard PEM format. |
| `dc_url` | `str` | Data Center endpoint URL (e.g. `https://messengerg2c332.iranlms.ir`). |
| `user_guid` | `Optional[str]` | Authenticated account GUID. |
| `phone` | `Optional[str]` | Authenticated phone number. |
| `is_authenticated` | `bool` | `True` if session has valid server auth credentials. |
| `file_path` | `Optional[str]` | Associated local session file path on disk (e.g. `bot.session`). |

### Methods
- `session.to_string() -> str`: Encodes session to portable base64 string (`RubiFlow$...`).
- `Session.from_string(session_string: str) -> Session`: Deserializes StringSession.
- `session.save(file_path: Optional[str] = None)`: Writes session to file.
- `Session.load_from_file(file_path: str) -> Session`: Loads session from JSON file.
- `Session.from_firefox() -> Session`: Decrypts active Firefox browser session.
- `Session.new_temporary(...) -> Session`: Creates unauthenticated temporary session for login.

---

## `FileMetadata`
Dictionary returned when requesting or completing file uploads via `upload_file`.

```python
{
    "file_id": "1049285712",
    "access_hash_send": "349102847501928471029384",
    "mime": "image/jpeg",
    "size": 245892,
    "file_name": "photo.jpg",
    "cdn_url": "https://storage.iranlms.ir/..."
}
```
