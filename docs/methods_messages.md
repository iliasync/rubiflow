# 💬 Messaging & Polls API

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
