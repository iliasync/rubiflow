# 📢 Channels & Broadcasts API

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
