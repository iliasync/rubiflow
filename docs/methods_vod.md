# 🎬 VOD Movies & Series API

Access Rubika's streaming media platform: movies, TV series, HLS streaming playlists, and cast filmography.

---

### `search_vod`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Searches the Rubika VOD entertainment catalog.

```python
results = await app.search_vod("Inception")
for movie in results:
    print(f"Title: {movie['title']} | ID: {movie['id']}")
```

---

### `get_vod_media` / `get_vod_play_info`
<span class="badge post">POST</span> <span class="badge async">Async</span>

- **`get_vod_media(media_id: str)`**: Fetches synopsis, genres, duration, and cover art.
- **`get_vod_play_info(media_id: str)`**: Returns HLS video stream playlist URLs (`.m3u8`) and playback tokens.

---

### TV Series & Episodes
- **`get_vod_season_episodes(series_id: str, season_id=None)`**: Lists episodes of a TV show with streaming links.

---

### Watchlist & Progress
- **`get_vod_wishlist()`**: Lists user's saved movies and shows.
- **`add_vod_wishlist(media_id: str)`**: Adds a title to watchlist.
- **`set_vod_play_time(media_id: str, play_time_seconds: int)`**: Synchronizes resume playback position across devices.
