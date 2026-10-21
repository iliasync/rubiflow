# 🎬 VOD Movies & Series API

Access Rubika's streaming entertainment platform: search movies and series, fetch HLS video stream playlists (`.m3u8`), manage watchlists, and view cast filmographies.

---

### `search_vod`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Searches the Rubika VOD video library.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `query` | `str` | Yes | - | Title, actor, or genre search term. |

#### Return Value
```python
results = await app.search_vod("Interstellar")
for item in results:
    print(f"Title: {item['title']} | Type: {item['type']} | ID: {item['id']}")
```

---

### `get_vod_media`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Retrieves full metadata for a movie or TV series.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `media_id` | `str` | Yes | - | Unique media identifier. |

#### Response Attributes
Includes synopsis, genres, duration, release year, IMDb rating, age rating, and thumbnail covers.

---

### `get_vod_play_info`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Returns direct HLS streaming playlist URLs (`.m3u8`), playback tokens, available resolutions (1080p, 720p, 480p, 360p), and subtitle tracks.

#### Code Example
```python
play_info = await app.get_vod_play_info("media_12345")
print(f"HLS Master Playlist: {play_info.get('play_url')}")
```

---

### `get_vod_season_episodes`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Lists all episodes and season breakdowns for a TV show.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `series_id` | `str` | Yes | - | Unique identifier of the TV show. |
| `season_id` | `str` | No | `None` | Optional season filter. |

---

### `get_vod_wishlist` / `add_vod_wishlist`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`get_vod_wishlist()`**: Lists all movies and shows saved to the user's watchlist.
- **`add_vod_wishlist(media_id: str)`**: Adds a title to the watchlist.

---

### `set_vod_play_time`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Synchronizes playback progress (resume point in seconds) across devices.
