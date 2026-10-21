"""
Account appearance, privacy, notification, and sticker settings methods.
"""

from typing import Any, Dict, List, Optional


class SettingsMethods:
    """Methods for account preferences, appearance, privacy, and sticker sets."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    async def get_appearance_setting(self) -> Dict[str, Any]:
        """Retrieves theme and bubble appearance settings."""
        res = await self.execute("getAppearanceSetting", {})
        return res.get("data", {}).get("appearance", {})

    async def set_appearance_setting(self, setting_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Updates theme and bubble appearance settings."""
        return await self.execute("setAppearanceSetting", {"appearance": setting_dict})

    async def get_privacy_setting(self) -> Dict[str, Any]:
        """Retrieves privacy visibility settings (phone number, last seen)."""
        res = await self.execute("getPrivacySetting", {})
        return res.get("data", {}).get("privacy", {})

    async def set_privacy_setting(self, privacy_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Updates privacy visibility settings."""
        return await self.execute("setPrivacySetting", {"privacy": privacy_dict})

    async def get_notification_setting(self) -> Dict[str, Any]:
        """Retrieves sound and notification preferences."""
        res = await self.execute("getNotificationSetting", {})
        return res.get("data", {}).get("notification", {})

    async def set_notification_setting(self, notification_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Updates notification sound and vibration preferences."""
        return await self.execute("setNotificationSetting", {"notification": notification_dict})

    async def get_my_sticker_sets(self) -> List[Dict[str, Any]]:
        """Retrieves installed sticker packs."""
        res = await self.execute("getMyStickerSets", {})
        return res.get("data", {}).get("sticker_sets", [])

    async def get_trend_sticker_sets(self) -> List[Dict[str, Any]]:
        """Retrieves trending sticker sets."""
        res = await self.execute("getTrendStickerSets", {})
        return res.get("data", {}).get("sticker_sets", [])

    async def action_on_sticker_set(
        self, sticker_set_id: str, action: str = "Add"
    ) -> Dict[str, Any]:
        """Adds or removes a sticker pack from favorites."""
        return await self.execute(
            "actionOnStickerSet",
            {"sticker_set_id": sticker_set_id, "action": action},
        )

    async def add_to_my_gif_set(self, gif_id: str) -> Dict[str, Any]:
        """Saves a GIF to account saved GIFs."""
        return await self.execute("addToMyGifSet", {"gif_id": gif_id})
