# 👤 Users & Contacts API

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
