"""
Rubino Social Network (Instagram clone) methods:
Explore, Posts, Stories, Highlights, Comments, Likes, and Followers.
"""

from typing import Any, Dict, List, Optional


class RubinoMethods:
    """Comprehensive Rubino social network API methods."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    # --- Feed & Explore ---

    async def get_rubino_explore(
        self,
        limit: int = 24,
        max_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieves infinite scroll explore posts."""
        payload: Dict[str, Any] = {"limit": limit}
        if max_id:
            payload["max_id"] = max_id
        return await self.execute("getExplorePosts", payload)

    async def get_explore_post_topics(self) -> List[Dict[str, Any]]:
        """Retrieves list of explore topic categories."""
        res = await self.execute("getExplorePostTopics", {})
        return res.get("data", {}).get("topics", [])

    async def get_related_explore_post(self, post_id: str) -> List[Dict[str, Any]]:
        """Retrieves recommended posts related to a viewed post."""
        res = await self.execute("getRelatedExplorePost", {"post_id": post_id})
        return res.get("data", {}).get("posts", [])

    async def get_recent_following_posts(
        self,
        limit: int = 20,
        max_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves timeline feed from followed profiles."""
        payload: Dict[str, Any] = {"limit": limit}
        if max_id:
            payload["max_id"] = max_id
        res = await self.execute("getRecentFollowingPosts", payload)
        return res.get("data", {}).get("posts", [])

    async def get_posts_by_hashtag(
        self,
        hashtag: str,
        limit: int = 20,
        max_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves posts containing a specific hashtag."""
        payload: Dict[str, Any] = {
            "hashtag": hashtag.lstrip("#"),
            "limit": limit,
        }
        if max_id:
            payload["max_id"] = max_id
        res = await self.execute("getPostsByHashTag", payload)
        return res.get("data", {}).get("posts", [])

    async def get_hashtag_trend(self) -> List[Dict[str, Any]]:
        """Retrieves current trending hashtags on Rubino."""
        res = await self.execute("getHashTagTrend", {})
        return res.get("data", {}).get("hashtags", [])

    # --- Profiles & Pages ---

    async def get_rubino_profile_info(self, profile_id: str) -> Dict[str, Any]:
        """Retrieves public Rubino profile info and follower counters."""
        res = await self.execute("getProfileInfo", {"profile_id": profile_id})
        return res.get("data", {}).get("profile", {})

    async def get_my_rubino_profile_info(self) -> Dict[str, Any]:
        """Retrieves user's own Rubino profile details."""
        res = await self.execute("getMyProfileInfo", {})
        return res.get("data", {}).get("profile", {})

    async def get_rubino_profile_posts(
        self,
        profile_id: str,
        limit: int = 20,
        max_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves grid posts for a Rubino creator profile."""
        payload: Dict[str, Any] = {
            "profile_id": profile_id,
            "limit": limit,
        }
        if max_id:
            payload["max_id"] = max_id
        res = await self.execute("getProfilePosts", payload)
        return res.get("data", {}).get("posts", [])

    async def create_rubino_page(
        self,
        name: str,
        username: str,
        bio: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates a new Rubino creator page."""
        payload: Dict[str, Any] = {
            "name": name,
            "username": username.lstrip("@"),
        }
        if bio:
            payload["bio"] = bio
        return await self.execute("createPage", payload)

    # --- Posts, Likes & Comments ---

    async def like_post(self, post_id: str, profile_id: str) -> Dict[str, Any]:
        """Likes a post."""
        return await self.execute(
            "likePostAction",
            {"post_id": post_id, "profile_id": profile_id, "action_type": "Like"},
        )

    async def unlike_post(self, post_id: str, profile_id: str) -> Dict[str, Any]:
        """Unlikes a previously liked post."""
        return await self.execute(
            "likePostAction",
            {"post_id": post_id, "profile_id": profile_id, "action_type": "Unlike"},
        )

    async def get_post_likes(self, post_id: str, profile_id: str) -> List[Dict[str, Any]]:
        """Retrieves list of profiles who liked a post."""
        res = await self.execute("getPostLikes", {"post_id": post_id, "profile_id": profile_id})
        return res.get("data", {}).get("profiles", [])

    async def bookmark_post(self, post_id: str, profile_id: str) -> Dict[str, Any]:
        """Saves a post to bookmarks."""
        return await self.execute(
            "postBookmarkAction",
            {"post_id": post_id, "profile_id": profile_id, "action_type": "Bookmark"},
        )

    async def unbookmark_post(self, post_id: str, profile_id: str) -> Dict[str, Any]:
        """Removes a post from bookmarks."""
        return await self.execute(
            "postBookmarkAction",
            {"post_id": post_id, "profile_id": profile_id, "action_type": "Unbookmark"},
        )

    async def get_bookmarked_posts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieves saved bookmark posts."""
        res = await self.execute("getBookmarkedPosts", {"limit": limit})
        return res.get("data", {}).get("posts", [])

    async def add_comment(
        self,
        post_id: str,
        profile_id: str,
        text: str,
    ) -> Dict[str, Any]:
        """Adds a comment on a post."""
        payload = {
            "post_id": post_id,
            "profile_id": profile_id,
            "content": text,
        }
        return await self.execute("addComment", payload)

    async def get_comments(
        self,
        post_id: str,
        profile_id: str,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Retrieves comments of a post."""
        payload = {
            "post_id": post_id,
            "profile_id": profile_id,
            "limit": limit,
        }
        res = await self.execute("getComments", payload)
        return res.get("data", {}).get("comments", [])

    async def like_comment(
        self,
        comment_id: str,
        post_id: str,
        profile_id: str,
    ) -> Dict[str, Any]:
        """Likes a comment."""
        payload = {
            "comment_id": comment_id,
            "post_id": post_id,
            "profile_id": profile_id,
            "action_type": "Like",
        }
        return await self.execute("likeCommentAction", payload)

    # --- Stories & Reels ---

    async def get_profiles_stories(self) -> List[Dict[str, Any]]:
        """Retrieves active stories feed for top bar."""
        res = await self.execute("getProfilesStories", {})
        return res.get("data", {}).get("stories", [])

    async def get_story(self, story_id: str, profile_id: str) -> Dict[str, Any]:
        """Retrieves single story media and caption."""
        return await self.execute("getStory", {"story_id": story_id, "profile_id": profile_id})

    async def add_view_story(self, story_id: str, profile_id: str) -> Dict[str, Any]:
        """Records a view event on a story."""
        return await self.execute("addViewStory", {"story_id": story_id, "profile_id": profile_id})

    async def delete_story(self, story_id: str, profile_id: str) -> Dict[str, Any]:
        """Deletes a story."""
        return await self.execute("deleteStory", {"story_id": story_id, "profile_id": profile_id})

    async def get_story_viewers(self, story_id: str, profile_id: str) -> List[Dict[str, Any]]:
        """Retrieves viewer profiles of a story."""
        res = await self.execute("getStoryViewers", {"story_id": story_id, "profile_id": profile_id})
        return res.get("data", {}).get("viewers", [])

    # --- Followers & Following ---

    async def request_follow(
        self,
        target_profile_id: str,
        action: str = "Follow",
    ) -> Dict[str, Any]:
        """
        Follows or un-follows a Rubino profile.
        action can be 'Follow' or 'Unfollow'.
        """
        return await self.execute(
            "requestFollow",
            {"target_profile_id": target_profile_id, "action": action},
        )

    async def get_profile_followers(
        self,
        profile_id: str,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Retrieves followers of a Rubino profile."""
        res = await self.execute("getProfileFollowers", {"profile_id": profile_id, "limit": limit})
        return res.get("data", {}).get("profiles", [])

    async def search_rubino_profile(self, search_text: str) -> List[Dict[str, Any]]:
        """Searches creator profiles on Rubino."""
        res = await self.execute("searchProfile", {"search_text": search_text})
        return res.get("data", {}).get("profiles", [])

    async def search_rubino_hashtag(self, search_text: str) -> List[Dict[str, Any]]:
        """Searches hashtags on Rubino."""
        res = await self.execute("searchHashTag", {"search_text": search_text})
        return res.get("data", {}).get("hashtags", [])
