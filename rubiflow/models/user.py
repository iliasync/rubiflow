"""
User and Profile models.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class User:
    """Represents a Rubika user account."""

    guid: str
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    is_deleted: bool = False
    is_verified: bool = False
    raw: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Instantiates a User from a Rubika raw API response dictionary."""
        return cls(
            guid=data.get("user_guid") or data.get("object_guid", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name"),
            username=data.get("username"),
            phone=data.get("phone"),
            bio=data.get("bio"),
            is_deleted=data.get("is_deleted", False),
            is_verified=data.get("is_verified", False),
            raw=data,
        )

    @property
    def full_name(self) -> str:
        """Returns the user's full name."""
        if self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.first_name or ""

    @property
    def mention(self) -> str:
        """Returns @username or markdown link."""
        if self.username:
            return f"@{self.username}"
        return self.full_name
