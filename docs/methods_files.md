# 📁 Cloud Files & CDN API

RubiFlow handles high-speed chunked uploading and downloading across Rubika's distributed media CDN clusters.

---

### `upload_file`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Uploads a local file or raw bytes to Rubika CDN nodes and returns file metadata ready to be attached to messages or posts.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `file_input` | `str \| bytes` | Yes | Local file path (`str`) or raw file contents in memory (`bytes`). |
| `file_name` | `str` | No | Explicit file name. If omitted, extracted from path. |
| `mime` | `str` | No | MIME type of the file. Defaults to `'application/octet-stream'`. |

#### Return Value
```python
{
    "file_id": "1234567890",
    "access_hash_send": "9876543210...",
    "mime": "image/jpeg",
    "size": 1048576,
    "file_name": "photo.jpg"
}
```

#### Code Example
```python
file_meta = await app.upload_file("wallpaper.jpg", mime="image/jpeg")
print(f"Uploaded File ID: {file_meta['file_id']}")
```

---

### `download_file`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Downloads a file from Rubika CDN using its `file_id` and `access_hash_rec`.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `file_id` | `str \| int` | Yes | File identifier. |
| `access_hash_rec` | `str` | Yes | Received access hash for the file. |
| `save_path` | `str` | No | Local destination file path. If `None`, returns raw `bytes`. |

#### Code Example
```python
# Download to disk
await app.download_file(file_id="12345", access_hash_rec="hash...", save_path="downloaded.png")

# Download to memory
data_bytes = await app.download_file(file_id="12345", access_hash_rec="hash...")
```

---

### Stickers
- **`get_trend_sticker_sets()`**: Retrieves list of trending sticker packs.
- **`get_my_sticker_sets()`**: Lists user's saved sticker collections.
