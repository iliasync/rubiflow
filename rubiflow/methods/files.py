"""
File upload, download, and profile avatar management methods.
"""

import os
from typing import Any, Dict, List, Optional, Union
import aiohttp

from ..exceptions import FileError


class FilesMethods:
    """Methods for uploading/downloading media files and managing avatars."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    async def request_send_file(
        self,
        file_name: str,
        size: int,
        mime: str,
    ) -> Dict[str, Any]:
        """Requests upload token and assigned storage CDN endpoint for a file."""
        payload = {
            "file_name": file_name,
            "size": size,
            "mime": mime,
        }
        res = await self.execute("requestSendFile", payload)
        return res.get("data", {})

    async def get_avatars(self, object_guid: str) -> List[Dict[str, Any]]:
        """Retrieves list of avatars/profile photos for user, group, or channel."""
        res = await self.execute("getAvatars", {"object_guid": object_guid})
        return res.get("data", {}).get("avatars", [])

    async def delete_avatar(self, object_guid: str, avatar_id: str) -> Dict[str, Any]:
        """Deletes a profile photo."""
        return await self.execute(
            "deleteAvatar",
            {"object_guid": object_guid, "avatar_id": avatar_id},
        )

    async def upload_file(
        self,
        file_input: Union[str, bytes],
        file_name: Optional[str] = None,
        mime: str = "application/octet-stream",
    ) -> Dict[str, Any]:
        """
        Uploads a file to Rubika CDN nodes and returns file metadata.
        """
        if isinstance(file_input, str):
            if not os.path.exists(file_input):
                raise FileNotFoundError(f"File not found: {file_input}")
            with open(file_input, "rb") as f:
                data = f.read()
            if not file_name:
                file_name = os.path.basename(file_input)
        else:
            data = file_input
            if not file_name:
                file_name = "file.bin"

        file_size = len(data)
        file_ext = file_name.split(".")[-1].lower() if "." in file_name else "bin"

        # 1. Request upload node
        upload_meta = await self.request_send_file(file_name, file_size, file_ext)
        upload_url = upload_meta.get("upload_url")
        id_str = upload_meta.get("id")
        dc_id = upload_meta.get("dc_id")

        if not upload_url:
            raise FileError("Server did not return an upload_url.")

        # 2. Upload byte payload to CDN
        headers = {
            "auth": getattr(self, "session", None).auth if hasattr(self, "session") else "",
            "file-id": str(id_str),
            "chunk-size": str(file_size),
            "part-number": "1",
            "total-part": "1",
            "Content-Type": "application/octet-stream",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(upload_url, headers=headers, data=data) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise FileError(f"Upload failed with HTTP {resp.status}: {text}")
                result = await resp.json()
                return {
                    "file_id": id_str,
                    "dc_id": dc_id,
                    "size": file_size,
                    "mime": file_ext,
                    "access_hash_rec": result.get("data", {}).get("access_hash_rec"),
                }
