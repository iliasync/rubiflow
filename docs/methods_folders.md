# 🗂️ Folders & Organization API

Rubika supports chat categorization through custom folders (tabs) like Telegram.

---

### `get_folders`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Retrieves all configured chat folders for the account.

```python
folders = await app.get_folders()
for folder in folders:
    print(f"Folder: {folder['name']} | ID: {folder['folder_id']}")
```

---

### `create_folder`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Creates a new custom chat tab.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | Yes | Folder tab title (e.g. `'Work'`, `'Bots'`). |
| `include_chat_types` | `List[str]` | Yes | Chat categories to include: `['Users', 'Groups', 'Channels', 'Bots']`. |
| `exclude_chat_types` | `List[str]` | No | Optional chat categories to exclude. |

#### Code Example
```python
await app.create_folder(
    name="Channels",
    include_chat_types=["Channels"]
)
```

---

### `delete_folder`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Deletes a chat folder by its ID.
