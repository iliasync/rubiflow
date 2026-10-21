# 📸 Rubino Social Network API

Rubino is Rubika's built-in Instagram-style social platform. RubiFlow provides complete access to Rubino creators, explore feeds, likes, comments, and stories.

---

### `get_rubino_explore`
<span class="badge post">POST</span> <span class="badge async">Async</span>

Fetches the infinite-scroll Explore feed.

#### Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `limit` | `int` | No | Number of posts to retrieve (default `24`). |
| `max_id` | `str` | No | Pagination cursor. |

#### Code Example
```python
explore = await app.get_rubino_explore(limit=10)
for post in explore.get("posts", []):
    print(f"Post {post['id']} by @{post['profile']['username']}: {post.get('caption')}")
```

---

### `get_rubino_profile_info` / `get_rubino_profile_posts`
<span class="badge post">POST</span> <span class="badge async">Async</span>

- **`get_rubino_profile_info(profile_id: str)`**: Gets follower count, bio, and profile details.
- **`get_rubino_profile_posts(profile_id: str, limit=20, max_id=None)`**: Retrieves a creator's published grid posts.

---

### Interacting with Posts
- **`like_post(post_id: str, profile_id: str)`**: Likes a Rubino post.
- **`unlike_post(post_id: str, profile_id: str)`**: Unlikes a post.
- **`bookmark_post(post_id: str, profile_id: str)`**: Saves a post to bookmarks.
- **`unbookmark_post(post_id: str, profile_id: str)`**: Removes a post from bookmarks.

---

### Comments & Discussions
- **`add_comment(post_id: str, profile_id: str, content: str)`**: Posts a comment on a photo or video.
- **`like_comment(comment_id: str, post_id: str, profile_id: str)`**: Likes a comment.
- **`get_comments(post_id: str, profile_id: str, limit=20)`**: Lists comments on a post.

---

### Social Graph & Following
- **`request_follow(target_profile_id: str, action='Follow')`**: Follows or unfollows a creator profile (`'Follow'` or `'Unfollow'`).
- **`get_story(story_id: str, profile_id: str)`**: Fetches story media and viewer counts.
- **`get_story_viewers(story_id: str, profile_id: str)`**: Retrieves list of users who watched a story.

---

### Search
- **`search_rubino_profile(search_text: str)`**: Finds creators by name or username.
- **`search_rubino_hashtag(search_text: str)`**: Searches posts by hashtag.
