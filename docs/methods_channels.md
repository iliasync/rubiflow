# 📢 Channels & Broadcasts API

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
