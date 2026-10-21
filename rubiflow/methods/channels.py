"""
Channel creation, management, invite links, and subscriber moderation methods.
"""

from typing import Any, Dict, List, Optional


class ChannelsMethods:
    """Methods for channel administration, subscribers, and invite links."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    async def add_channel(
        self,
        title: str,
        description: Optional[str] = None,
        channel_type: str = "Public",
    ) -> Dict[str, Any]:
        """Creates a new broadcast channel."""
        payload: Dict[str, Any] = {
            "title": title,
            "channel_type": channel_type,
        }
        if description:
            payload["description"] = description
        return await self.execute("addChannel", payload)

    async def get_channel_info(self, channel_guid: str) -> Dict[str, Any]:
        """Retrieves channel metadata, subscriber count, bio, and username."""
        res = await self.execute("getChannelInfo", {"channel_guid": channel_guid})
        return res.get("data", {}).get("channel", {})

    async def edit_channel_info(
        self,
        channel_guid: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Updates channel title and description."""
        payload: Dict[str, Any] = {"channel_guid": channel_guid}
        if title:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        return await self.execute("editChannelInfo", payload)

    async def get_channel_members(
        self,
        channel_guid: str,
        start_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves paginated list of channel subscribers."""
        payload: Dict[str, Any] = {"channel_guid": channel_guid}
        if start_id:
            payload["start_id"] = start_id
        res = await self.execute("getChannelMembers", payload)
        return res.get("data", {}).get("in_chat_members", [])

    async def add_channel_members(
        self,
        channel_guid: str,
        member_guids: List[str],
    ) -> Dict[str, Any]:
        """Adds subscribers to a channel."""
        return await self.execute(
            "addChannelMembers",
            {"channel_guid": channel_guid, "member_guids": member_guids},
        )

    async def ban_channel_member(
        self,
        channel_guid: str,
        member_guid: str,
    ) -> Dict[str, Any]:
        """Removes and bans a subscriber from a channel."""
        return await self.execute(
            "banChannelMember",
            {"channel_guid": channel_guid, "member_guid": member_guid, "action": "Set"},
        )

    async def set_channel_admin(
        self,
        channel_guid: str,
        member_guid: str,
        access_list: List[str],
        action: str = "SetAdmin",
    ) -> Dict[str, Any]:
        """Promotes subscriber to channel administrator."""
        payload = {
            "channel_guid": channel_guid,
            "member_guid": member_guid,
            "access_list": access_list,
            "action": action,
        }
        return await self.execute("setChannelAdmin", payload)

    async def get_channel_admin_members(self, channel_guid: str) -> List[Dict[str, Any]]:
        """Retrieves list of channel administrators."""
        res = await self.execute("getChannelAdminMembers", {"channel_guid": channel_guid})
        return res.get("data", {}).get("in_chat_members", [])

    async def channel_preview_by_join_link(self, invite_link: str) -> Dict[str, Any]:
        """Retrieves public preview of a channel from an invite link."""
        hash_slug = invite_link.split("/")[-1]
        res = await self.execute("channelPreviewByJoinLink", {"hash_link": hash_slug})
        return res.get("data", {})

    async def join_channel_by_link(self, invite_link: str) -> Dict[str, Any]:
        """Joins a channel via invite link."""
        hash_slug = invite_link.split("/")[-1]
        return await self.execute("joinChannelByLink", {"hash_link": hash_slug})

    async def create_join_link(self, channel_guid: str) -> Dict[str, Any]:
        """Generates an invitation link for a channel."""
        return await self.execute("createJoinLink", {"object_guid": channel_guid})

    async def edit_join_link(
        self, channel_guid: str, link_id: str, is_active: bool = True
    ) -> Dict[str, Any]:
        """Modifies settings or activates/deactivates an invite link."""
        payload = {
            "object_guid": channel_guid,
            "link_id": link_id,
            "is_active": is_active,
        }
        return await self.execute("editJoinLink", payload)

    async def delete_revoked_join_link(
        self, channel_guid: str, link_id: str
    ) -> Dict[str, Any]:
        """Deletes an expired or revoked invitation link."""
        return await self.execute(
            "deleteRevokedJoinLink",
            {"object_guid": channel_guid, "link_id": link_id},
        )

    async def action_on_join_request(
        self, channel_guid: str, user_guid: str, action: str = "Accept"
    ) -> Dict[str, Any]:
        """Accepts or rejects a user's join request to a private channel."""
        payload = {
            "object_guid": channel_guid,
            "user_guid": user_guid,
            "action": action,
        }
        return await self.execute("actionOnJoinRequest", payload)

    async def check_channel_username(self, username: str) -> bool:
        """Checks if a channel @username is available."""
        clean_user = username.lstrip("@")
        res = await self.execute("checkChannelUsername", {"username": clean_user})
        return bool(res.get("data", {}).get("is_exist") is False)

    async def update_channel_username(
        self, channel_guid: str, username: str
    ) -> Dict[str, Any]:
        """Sets or updates the public @username of a channel."""
        clean_user = username.lstrip("@")
        return await self.execute(
            "updateChannelUsername",
            {"channel_guid": channel_guid, "username": clean_user},
        )

    async def leave_channel(self, channel_guid: str) -> Dict[str, Any]:
        """Leaves and un-subscribes from a channel."""
        return await self.execute("leaveChannel", {"channel_guid": channel_guid})
