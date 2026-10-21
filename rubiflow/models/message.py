"""
Message model.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..client import Client


@dataclass
class Message:
    """Represents a Rubika message."""

    message_id: str
    chat_guid: str
    author_guid: str
    text: str
    time: int
    is_edited: bool = False
    reply_to_message_id: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None
    _client: Optional["Client"] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any], client: Optional["Client"] = None) -> "Message":
        """Instantiates a Message from raw message dictionary."""
        return cls(
            message_id=str(data.get("message_id", "")),
            chat_guid=data.get("object_guid") or data.get("chat_guid", ""),
            author_guid=data.get("author_object_guid", ""),
            text=data.get("text", "") or "",
            time=int(data.get("time", 0)),
            is_edited=bool(data.get("is_edited", False)),
            reply_to_message_id=str(data.get("reply_to_message_id")) if data.get("reply_to_message_id") else None,
            raw=data,
            _client=client,
        )

    async def reply(self, text: str) -> "Message":
        """Convenience method to reply to this message."""
        if not self._client:
            raise RuntimeError("Client not bound to message instance.")
        return await self._client.send_message(
            target=self.chat_guid,
            text=text,
            reply_to_message_id=self.message_id,
        )

    async def delete(self) -> None:
        """Deletes this message."""
        if not self._client:
            raise RuntimeError("Client not bound to message instance.")
        await self._client.delete_messages(
            chat_guid=self.chat_guid,
            message_ids=[self.message_id],
        )

    async def edit(self, text: str) -> "Message":
        """Edits this message."""
        if not self._client:
            raise RuntimeError("Client not bound to message instance.")
        return await self._client.edit_message(
            chat_guid=self.chat_guid,
            message_id=self.message_id,
            text=text,
        )
