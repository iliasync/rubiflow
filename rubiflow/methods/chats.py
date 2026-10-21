"""
Chat and dialog management methods.
"""

from typing import Any, Dict, List, Optional

from ..models import Chat


class ChatsMethods:
    """Methods for dialog listing, chat history management, and read receipts."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    async def get_chats(self, start_id: Optional[str] = None) -> List[Chat]:
        """Retrieves paginated list of conversations and dialogs."""
        payload: Dict[str, Any] = {}
        if start_id:
            payload["start_id"] = start_id
        res = await self.execute("getChats", payload)
        raw_chats = res.get("data", {}).get("chats", [])
        return [Chat.from_dict(c) for c in raw_chats]

    async def get_chats_updates(self, state: int) -> Dict[str, Any]:
        """Fetches realtime chat list changes since sync state."""
        return await self.execute("getChatsUpdates", {"state": state})

    async def get_chats_by_id(self, object_guids: List[str]) -> List[Chat]:
        """Retrieves specific chats by their object GUIDs."""
        res = await self.execute("getChatsByID", {"object_guids": object_guids})
        raw_chats = res.get("data", {}).get("chats", [])
        return [Chat.from_dict(c) for c in raw_chats]

    async def seen_chats(self, seen_map: Dict[str, int]) -> Dict[str, Any]:
        """
        Marks messages in chats as read.
        seen_map is a dictionary of {chat_guid: last_seen_message_id}.
        """
        return await self.execute("seenChats", {"seen_chats": seen_map})

    async def delete_chat_history(
        self,
        target: str,
        last_message_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Clears message history of a conversation."""
        payload: Dict[str, Any] = {"object_guid": target}
        if last_message_id:
            payload["last_message_id"] = str(last_message_id)
        return await self.execute("deleteChatHistory", payload)

    async def delete_user_chat(self, user_guid: str) -> Dict[str, Any]:
        """Deletes a direct 1-to-1 conversation with a user."""
        return await self.execute("deleteUserChat", {"user_guid": user_guid})

    async def delete_group_chat(self, group_guid: str) -> Dict[str, Any]:
        """Leaves and deletes a group conversation."""
        return await self.execute("deleteGroupChat", {"group_guid": group_guid})

    async def delete_channel_chat(self, channel_guid: str) -> Dict[str, Any]:
        """Leaves and deletes a channel from dialogs."""
        return await self.execute("deleteChannelChat", {"channel_guid": channel_guid})

    async def delete_service_chat(self, service_guid: str) -> Dict[str, Any]:
        """Deletes a service notifications chat."""
        return await self.execute("deleteServiceChat", {"service_guid": service_guid})

    async def delete_bot_chat(self, bot_guid: str) -> Dict[str, Any]:
        """Deletes a bot conversation."""
        return await self.execute("deleteBotChat", {"bot_guid": bot_guid})

    async def search_chats(self, search_text: str) -> List[Chat]:
        """Searches chat titles and dialogs."""
        res = await self.execute("searchChats", {"search_text": search_text})
        raw_chats = res.get("data", {}).get("chats", [])
        return [Chat.from_dict(c) for c in raw_chats]

    async def get_chat_ads(self, state: int = 0) -> Dict[str, Any]:
        """Retrieves sponsored message ads for dialog list."""
        return await self.execute("getChatAds", {"state": state})
