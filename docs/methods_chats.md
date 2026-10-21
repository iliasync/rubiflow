# 💬 Chats & Dialogs API

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
