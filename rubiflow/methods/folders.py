"""
Chat Folders and Tabs management methods.
"""

from typing import Any, Dict, List, Optional


class FoldersMethods:
    """Methods for creating and managing custom chat folders and tabs."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    async def get_folders(self) -> List[Dict[str, Any]]:
        """Retrieves list of all user chat folders."""
        res = await self.execute("getFolders", {})
        return res.get("data", {}).get("folders", [])

    async def add_folder(
        self,
        name: str,
        include_chat_types: Optional[List[str]] = None,
        exclude_chat_types: Optional[List[str]] = None,
        include_guids: Optional[List[str]] = None,
        exclude_guids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Creates a custom chat folder."""
        payload: Dict[str, Any] = {
            "name": name,
            "include_chat_types": include_chat_types or ["User", "Group", "Channel"],
            "exclude_chat_types": exclude_chat_types or [],
            "include_object_guids": include_guids or [],
            "exclude_object_guids": exclude_guids or [],
        }
        return await self.execute("addFolder", payload)

    async def edit_folder(
        self,
        folder_id: str,
        name: Optional[str] = None,
        include_chat_types: Optional[List[str]] = None,
        exclude_chat_types: Optional[List[str]] = None,
        include_guids: Optional[List[str]] = None,
        exclude_guids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Edits an existing chat folder."""
        payload: Dict[str, Any] = {"folder_id": folder_id}
        if name:
            payload["name"] = name
        if include_chat_types is not None:
            payload["include_chat_types"] = include_chat_types
        if exclude_chat_types is not None:
            payload["exclude_chat_types"] = exclude_chat_types
        if include_guids is not None:
            payload["include_object_guids"] = include_guids
        if exclude_guids is not None:
            payload["exclude_object_guids"] = exclude_guids
        return await self.execute("editFolder", payload)

    async def delete_folder(self, folder_id: str) -> Dict[str, Any]:
        """Deletes a chat folder."""
        return await self.execute("deleteFolder", {"folder_id": folder_id})
