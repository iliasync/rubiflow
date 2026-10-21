"""
VOD (Video on Demand / Movies & Series) streaming methods.
"""

from typing import Any, Dict, List, Optional


class VodMethods:
    """Methods for Rubika streaming movies, series, episodes, and watchlists."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    async def get_vod_media(self, media_id: str) -> Dict[str, Any]:
        """Retrieves movie/series details and HLS stream playlist URLs."""
        res = await self.execute("vod-get-media", {"media_id": media_id})
        return res.get("data", {}).get("media", {})

    async def get_vod_play_info(self, media_id: str) -> Dict[str, Any]:
        """Retrieves playback tokens, resolutions, and streaming licenses."""
        return await self.execute("vod-get-play-info", {"media_id": media_id})

    async def get_vod_season_episodes(
        self,
        series_id: str,
        season_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves series episodes list."""
        payload: Dict[str, Any] = {"series_id": series_id}
        if season_id:
            payload["season_id"] = season_id
        res = await self.execute("vod-get-season-episodes", payload)
        return res.get("data", {}).get("episodes", [])

    async def get_vod_related(self, media_id: str) -> List[Dict[str, Any]]:
        """Retrieves related recommendations for a movie or series."""
        res = await self.execute("vod-get-related", {"media_id": media_id})
        return res.get("data", {}).get("medias", [])

    async def get_vod_wishlist(self) -> List[Dict[str, Any]]:
        """Retrieves user's saved movie/series watchlist."""
        res = await self.execute("vod-get-wish-list", {})
        return res.get("data", {}).get("medias", [])

    async def search_vod(self, query: str) -> List[Dict[str, Any]]:
        """Searches the Rubika VOD catalog."""
        res = await self.execute("vod-search", {"query": query})
        return res.get("data", {}).get("medias", [])

    async def set_vod_play_time(self, media_id: str, play_time_seconds: int) -> Dict[str, Any]:
        """Synchronizes watch progress position."""
        return await self.execute(
            "vod-set-current-play-time",
            {"media_id": media_id, "play_time": play_time_seconds},
        )

    async def get_vod_cast_details(self, cast_id: str) -> Dict[str, Any]:
        """Retrieves actor/director biography and filmography."""
        return await self.execute("vod-get-cast-details", {"cast_id": cast_id})
