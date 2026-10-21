# 🗂️ Folders & Organization API

Methods for creating, retrieving, and organizing custom chat folders and filter tabs like Telegram.

---

### `get_folders`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Retrieves all configured chat folders for the user's account.

#### Return Value
Returns a list of folder dictionaries:
```python
folders = await app.get_folders()
for folder in folders:
    print(f"Folder: {folder.get('name')} (ID: {folder.get('folder_id')})")
```

---

### `create_folder`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Creates a new custom chat tab.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `str` | Yes | - | Tab title (e.g. `'Work'`, `'Channels'`, `'Bots'`). |
| `include_chat_types` | `List[str]` | Yes | - | Chat categories to include: `['Users', 'Groups', 'Channels', 'Bots']`. |
| `exclude_chat_types` | `List[str]` | No | `None` | Optional chat categories to exclude. |

#### Code Example
```python
await app.create_folder(
    name="Channels",
    include_chat_types=["Channels"]
)
```

---

### `delete_folder`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Deletes a chat folder by its unique ID.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `folder_id` | `str` | Yes | - | Folder identifier. |
