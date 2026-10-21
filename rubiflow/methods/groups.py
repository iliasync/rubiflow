"""
Group and Supergroup management methods, including Voice Chat spaces.
"""

from typing import Any, Dict, List, Optional


class GroupsMethods:
    """Methods for group creation, administration, member moderation, and voice chats."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    async def add_group(
        self,
        title: str,
        member_guids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Creates a new group."""
        payload: Dict[str, Any] = {"title": title}
        if member_guids:
            payload["member_guids"] = member_guids
        return await self.execute("addGroup", payload)

    async def get_group_info(self, group_guid: str) -> Dict[str, Any]:
        """Retrieves group metadata, title, avatar, and description."""
        res = await self.execute("getGroupInfo", {"group_guid": group_guid})
        return res.get("data", {}).get("group", {})

    async def edit_group_info(
        self,
        group_guid: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Updates group title or description."""
        payload: Dict[str, Any] = {"group_guid": group_guid}
        if title:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        return await self.execute("editGroupInfo", payload)

    async def get_group_members(
        self,
        group_guid: str,
        start_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves paginated list of group members."""
        payload: Dict[str, Any] = {"group_guid": group_guid}
        if start_id:
            payload["start_id"] = start_id
        res = await self.execute("getGroupMembers", payload)
        return res.get("data", {}).get("in_chat_members", [])

    async def add_group_members(
        self,
        group_guid: str,
        member_guids: List[str],
    ) -> Dict[str, Any]:
        """Adds members to a group."""
        return await self.execute(
            "addGroupMembers",
            {"group_guid": group_guid, "member_guids": member_guids},
        )

    async def ban_group_member(
        self,
        group_guid: str,
        member_guid: str,
    ) -> Dict[str, Any]:
        """Bans and removes a member from a group."""
        return await self.execute(
            "banGroupMember",
            {"group_guid": group_guid, "member_guid": member_guid, "action": "Set"},
        )

    async def set_group_admin(
        self,
        group_guid: str,
        member_guid: str,
        access_list: List[str],
        action: str = "SetAdmin",
    ) -> Dict[str, Any]:
        """
        Promotes a member to administrator with custom permissions.
        action can be 'SetAdmin' or 'UnsetAdmin'.
        """
        payload = {
            "group_guid": group_guid,
            "member_guid": member_guid,
            "access_list": access_list,
            "action": action,
        }
        return await self.execute("setGroupAdmin", payload)

    async def get_group_admin_members(self, group_guid: str) -> List[Dict[str, Any]]:
        """Retrieves list of group administrators."""
        res = await self.execute("getGroupAdminMembers", {"group_guid": group_guid})
        return res.get("data", {}).get("in_chat_members", [])

    async def get_group_admin_access_list(
        self, group_guid: str, member_guid: str
    ) -> List[str]:
        """Retrieves the list of permissions granted to an administrator."""
        res = await self.execute(
            "getGroupAdminAccessList",
            {"group_guid": group_guid, "member_guid": member_guid},
        )
        return res.get("data", {}).get("access_list", [])

    async def set_group_default_access(
        self,
        group_guid: str,
        default_access: List[str],
    ) -> Dict[str, Any]:
        """Configures default permissions for regular group members."""
        return await self.execute(
            "setGroupDefaultAccess",
            {"group_guid": group_guid, "default_access": default_access},
        )

    async def get_group_default_access(self, group_guid: str) -> List[str]:
        """Retrieves default permissions configured for a group."""
        res = await self.execute("getGroupDefaultAccess", {"group_guid": group_guid})
        return res.get("data", {}).get("default_access", [])

    async def leave_group(self, group_guid: str) -> Dict[str, Any]:
        """Leaves a group."""
        return await self.execute("leaveGroup", {"group_guid": group_guid})

    # --- Group Voice Chats ---

    async def create_group_voice_chat(self, group_guid: str) -> Dict[str, Any]:
        """Starts a live audio voice room in a group."""
        return await self.execute("createGroupVoiceChat", {"group_guid": group_guid})

    async def discard_group_voice_chat(
        self, group_guid: str, voice_chat_id: str
    ) -> Dict[str, Any]:
        """Ends an active group voice chat room."""
        return await self.execute(
            "discardGroupVoiceChat",
            {"group_guid": group_guid, "voice_chat_id": voice_chat_id},
        )

    async def join_group_voice_chat(
        self, group_guid: str, voice_chat_id: str, sdp_offer: str
    ) -> Dict[str, Any]:
        """Joins an active voice chat room with WebRTC SDP offer."""
        payload = {
            "group_guid": group_guid,
            "voice_chat_id": voice_chat_id,
            "sdp_offer": sdp_offer,
        }
        return await self.execute("joinGroupVoiceChat", payload)

    async def get_group_voice_chat(
        self, group_guid: str, voice_chat_id: str
    ) -> Dict[str, Any]:
        """Retrieves current participants and stream details of a voice chat."""
        return await self.execute(
            "getGroupVoiceChat",
            {"group_guid": group_guid, "voice_chat_id": voice_chat_id},
        )

    async def get_group_voice_chat_updates(
        self, group_guid: str, voice_chat_id: str, state: int
    ) -> Dict[str, Any]:
        """Polls participant speaking status updates in a voice room."""
        payload = {
            "group_guid": group_guid,
            "voice_chat_id": voice_chat_id,
            "state": state,
        }
        return await self.execute("getGroupVoiceChatUpdates", payload)
