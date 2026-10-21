# 👥 Groups & Voice Chats API

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
