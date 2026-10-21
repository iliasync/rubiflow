# 💬 Chats & Dialogs API

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
