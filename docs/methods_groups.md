# 👥 Groups & Voice Chats API

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
