# ⚙️ Settings, 2FA & Privacy API

Complete reference for managing account security, Two-Step Verification (2FA), privacy visibility, themes, and active device sessions.

---

### `setup_two_step_verification`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Enables Two-Step Verification by setting a master password. Once enabled, logging into the account requires entering this password after the SMS code.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `password` | `str` | Yes | - | Master password to be set. |
| `hint` | `str` | No | `None` | Optional password hint to remind the user. |
| `recovery_email` | `str` | No | `None` | Optional recovery email to reset password if forgotten. |

#### Code Example
```python
await app.setup_two_step_verification(
    password="super_secure_password_123",
    hint="Favorite book character",
    recovery_email="user@example.com"
)
```

---

### `check_two_step_passcode`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Validates the user's Two-Step Verification password during login or when confirming sensitive operations.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `password` | `str` | Yes | - | Account 2FA password. |

#### Return Value
```json
{
  "status": "OK",
  "data": {
    "auth": "permanent_auth_token_32chars...",
    "user": {
      "user_guid": "u0ABCDEF1234567890",
      "first_name": "Mahan"
    }
  }
}
```

---

### `change_password`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Changes an existing Two-Step Verification password.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `old_password` | `str` | Yes | - | The current 2FA password. |
| `new_password` | `str` | Yes | - | The new 2FA password. |
| `hint` | `str` | No | `None` | New password hint. |

---

### `set_recovery_email` / `verify_recovery_email`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`set_recovery_email(email: str)`**: Requests sending a verification code to a recovery email address.
- **`verify_recovery_email(email_code: str)`**: Confirms the received verification code to bind the recovery email.

---

### `get_privacy_settings` / `set_privacy_setting`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Queries or modifies who can see your last seen status, profile photos, phone number, or add you to groups.

#### Options
Allowed visibility rules: `'Everybody'`, `'MyContacts'`, `'Nobody'`.

#### Code Example
```python
# Get current privacy rules
privacy = await app.get_privacy_settings()
print(privacy)

# Update last seen to contacts only
await app.set_privacy_setting({
    "last_seen_type": "MyContacts",
    "phone_number_type": "Nobody"
})
```

---

### `get_notification_settings` / `set_notification_setting`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Controls push notifications, sound, vibration, and message previews for Private Chats, Groups, and Channels.

#### Code Example
```python
await app.set_notification_setting({
    "users_mute": False,
    "groups_mute": True,
    "channels_mute": True
})
```

---

### `get_appearance_settings` / `set_appearance_setting`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Controls app color themes (Dark, Light, System) and message bubble font scale.

---

### Active Sessions Management

- **`get_my_sessions() -> List[Dict[str, Any]]`**: Retrieves a list of all active sessions, including device model, IP address, system version, and last active timestamp.
- **`terminate_session(session_key: str)`**: Terminates a specific device session by its unique session key.
- **`terminate_user_sessions()`**: Terminates all other logged-in sessions except the current one.
