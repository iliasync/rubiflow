# 👤 Users & Contacts API

Methods for querying user profiles, blocking/unblocking accounts, managing address books, and reserving usernames.

---

### `get_me`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Returns basic information about the currently authenticated user.

#### Return Value
Returns a [`User`](#user-object) object.

#### Code Example
```python
me = await app.get_me()
print(f"Hello, {me.first_name} (@{me.username})! GUID: {me.guid}")
```

---

### `get_user_info`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Fetches a user profile, online status, bio, and avatar by their user GUID.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `user_guid` | `str` | Yes | Target user GUID (`u...`). |

#### Return Value
Returns a [`User`](#user-object) object.

#### Code Example
```python
user = await app.get_user_info("u0ABCDEF123456789")
print(f"User: {user.first_name} {user.last_name}")
print(f"Bio: {user.bio}")
print(f"Online: {user.is_online}")
```

---

### `update_profile`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Updates the user's first name, last name, or bio.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `first_name` | `str` | No | New first name. |
| `last_name` | `str` | No | New last name. |
| `bio` | `str` | No | New bio description (up to 70 characters). |

---

### `update_username` / `check_username`
<span class="badge post">POST</span> <span class="badge async">Async</span>

- **`check_username(username: str)`**: Checks if a handle is available on Rubika.
- **`update_username(username: str)`**: Reserves and claims the handle for the authenticated account.

---

### `block_user` / `unblock_user` / `get_blocked_users`
<span class="badge post">POST</span> <span class="badge async">Async</span>

- **`block_user(user_guid: str)`**: Blocks incoming messages and calls from a user.
- **`unblock_user(user_guid: str)`**: Unblocks a previously blocked user.
- **`get_blocked_users()`**: Lists all blocked contacts.

---

### Address Book Synchronization
- **`get_contacts()`**: Retrieves synced phone contacts.
- **`add_address_book(first_name, last_name, phone)`**: Adds a new contact by phone number.
- **`delete_contact(user_guid)`**: Deletes a contact from the address book.
