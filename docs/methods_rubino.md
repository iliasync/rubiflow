# 📸 Rubino Social Network API

Comprehensive reference for interacting with Rubino, Rubika's built-in Instagram-style social media platform.

---

### `get_rubino_explore`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Fetches the infinite-scroll Explore feed containing popular photos, videos, and reels.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | No | `24` | Number of explore posts to retrieve. |
| `max_id` | `str` | No | `None` | Cursor for pagination offset. |

#### Code Example
```python
explore = await app.get_rubino_explore(limit=10)
for post in explore.get("posts", []):
    profile = post.get("profile", {})
    print(f"Post {post['id']} by @{profile.get('username')}: {post.get('caption')}")
```

---

### `get_rubino_profile_info`
<span class="badge badge-post">POST</span> <span class="badge async">Async</span>

Fetches complete public information about a creator profile on Rubino.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `profile_id` | `str` | Yes | - | Unique profile ID of the creator. |

#### Return Value
```json
{
  "profile": {
    "id": "p0ABCDEF...",
    "username": "creator_name",
    "name": "Mahan",
    "bio": "Developer and Content Creator",
    "count_followers": 1420,
    "count_following": 250,
    "count_posts": 45,
    "is_private": false,
    "is_verified": true
  }
}
```

---

### `get_rubino_profile_posts`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Retrieves a creator's published grid posts with pagination.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `profile_id` | `str` | Yes | - | Creator profile ID. |
| `limit` | `int` | No | `20` | Maximum number of posts to fetch. |
| `max_id` | `str` | No | `None` | Pagination cursor. |

---

### `like_post` / `unlike_post`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Likes or un-likes a post on Rubino.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `post_id` | `str` | Yes | - | Unique identifier of the post. |
| `profile_id` | `str` | Yes | - | Profile ID of the post author. |

#### Code Example
```python
await app.like_post(post_id="12345678", profile_id="p0ABCDEF...")
```

---

### `bookmark_post` / `unbookmark_post`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Saves or removes a post from your private saved bookmarks collection.

---

### `add_comment` / `like_comment` / `get_comments`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`add_comment(post_id: str, profile_id: str, content: str)`**: Submits a text comment on a post.
- **`like_comment(comment_id: str, post_id: str, profile_id: str)`**: Likes a specific comment.
- **`get_comments(post_id: str, profile_id: str, limit: int = 20)`**: Fetches comments list with author details.

---

### `request_follow`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

Follows or unfollows a creator profile.

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `target_profile_id` | `str` | Yes | - | Target profile to follow. |
| `action` | `str` | No | `'Follow'` | `'Follow'` or `'Unfollow'`. |

---

### `get_story` / `get_story_viewers`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`get_story(story_id: str, profile_id: str)`**: Fetches media URL, duration, and viewers counter for a story.
- **`get_story_viewers(story_id: str, profile_id: str)`**: Lists users who have viewed your story.

---

### `search_rubino_profile` / `search_rubino_hashtag`
<span class="badge badge-post">POST</span> <span class="badge badge-async">Async</span>

- **`search_rubino_profile(search_text: str)`**: Searches creators by username or display name.
- **`search_rubino_hashtag(search_text: str)`**: Searches posts tagged with a specific hashtag without `#`.
