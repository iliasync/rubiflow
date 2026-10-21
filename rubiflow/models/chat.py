"""
Chat and Dialog models.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Chat:
    """Represents a Rubika chat (User direct chat, Group, or Channel)."""

    guid: str
    type: str
    title: Optional[str] = None
    last_message_id: Optional[str] = None
    unread_count: int = 0
    raw: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chat":
        """Instantiates a Chat from a Rubika raw API response dictionary."""
        return cls(
            guid=data.get("object_guid", ""),
            type=data.get("type", "User"),
            title=data.get("title") or (data.get("last_message", {}) or {}).get("author_title"),
            last_message_id=str(data.get("last_message_id", "")),
            unread_count=int(data.get("count_unseen", 0)),
            raw=data,
        )

    @property
    def is_user(self) -> bool:
        return self.type == "User"

    @property
    def is_group(self) -> bool:
        return self.type == "Group"

    @property
    def is_channel(self) -> bool:
        return self.type == "Channel"
