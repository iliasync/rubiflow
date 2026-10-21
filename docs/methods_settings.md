# ⚙️ Settings & Privacy API

Manage account security, two-step verification, appearance themes, and active login sessions.

---

### Two-Step Verification (2FA)
- **`setup_two_step_verification(password, hint=None, recovery_email=None)`**: Sets a master password for login.
- **`set_recovery_email(email)`**: Configures a recovery email address.
- **`verify_recovery_email(email_code)`**: Confirms the email verification code.

---

### Privacy & Notifications
- **`get_privacy_settings()`** / **`set_privacy_setting(privacy_dict)`**: Configures who can see last seen status, phone number, and profile pictures (`Everybody`, `MyContacts`, `Nobody`).
- **`get_notification_settings()`** / **`set_notification_setting(notification_dict)`**: Controls sound, preview, and vibration.
- **`get_appearance_settings()`** / **`set_appearance_setting(setting_dict)`**: Controls theme (Dark, Light) and text scaling.

---

### Active Sessions Management
- **`terminate_session(session_key: str)`**: Terminates a specific device login.
- **`terminate_user_sessions()`**: Logs out all other active sessions except the current one.
