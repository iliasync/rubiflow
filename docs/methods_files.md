# 📁 Cloud Files, CDN & Stickers API

RubiFlow handles high-speed uploading and downloading across Rubika's distributed media CDN storage clusters.

---

### `upload_file`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Uploads a local file or in-memory byte buffer to Rubika CDN nodes and returns file metadata ready to be attached to messages or posts.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `file_input` | `Union[str, bytes]` | Yes | - | File path on disk (`str`) or raw file bytes in memory (`bytes`). |
| `file_name` | `str` | No | `None` | Custom file name. If omitted, derived from path or generated. |
| `mime` | `str` | No | `'application/octet-stream'` | MIME type (e.g. `'image/jpeg'`, `'video/mp4'`). |

#### Return Value
Returns a file metadata dictionary:
```json
{
  "file_id": "1049285712",
  "access_hash_send": "349102847501928471029384",
  "mime": "image/png",
  "size": 492048,
  "file_name": "screenshot.png",
  "cdn_url": "https://storage.iranlms.ir/..."
}
```

#### Code Example
```python
# Upload from disk path
meta = await app.upload_file("charts/report.pdf", mime="application/pdf")
print(f"Uploaded file ID: {meta['file_id']}")

# Upload in-memory bytes
import io
bio = io.BytesIO(b"Hello Rubika Cloud File")
meta2 = await app.upload_file(bio.getvalue(), file_name="memo.txt", mime="text/plain")
```

---

### `download_file`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Downloads a media file or document from Rubika CDN nodes.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `file_id` | `Union[str, int]` | Yes | - | Unique file identifier. |
| `access_hash_rec` | `str` | Yes | - | Received access hash for the file. |
| `save_path` | `str` | No | `None` | Local destination file path. If `None`, returns raw `bytes`. |

#### Code Example
```python
# Download and save to disk
await app.download_file(
    file_id="1049285712",
    access_hash_rec="349102847501928471029384",
    save_path="downloads/photo.jpg"
)

# Download into memory as bytes
file_bytes = await app.download_file(
    file_id="1049285712",
    access_hash_rec="349102847501928471029384"
)
print("Downloaded size:", len(file_bytes), "bytes")
```

---

### `request_send_file`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Low-level method to request an upload token and assigned storage CDN endpoint for a file before streaming chunks.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `file_name` | `str` | Yes | - | File name. |
| `size` | `int` | Yes | - | Size of the file in bytes. |
| `mime` | `str` | Yes | - | MIME type. |

---

### Sticker Packs

- **`get_trend_sticker_sets() -> List[Dict[str, Any]]`**: Retrieves a list of trending and featured sticker sets.
- **`get_my_sticker_sets() -> List[Dict[str, Any]]`**: Lists the user's saved sticker pack collections.
