"""
User profile, Contact synchronization, and Account management methods.
"""

from typing import Any, Dict, List, Optional

from ..models import User


class UsersMethods:
    """Methods for user profiles, contacts sync, blocking, and account settings."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    async def get_me(self) -> User:
        """Retrieves profile of the currently logged-in account."""
        res = await self.execute("getUserInfo", {})
        user_dict = res.get("data", {}).get("user", {})
        user = User.from_dict(user_dict)
        setattr(self, "_me", user)
        return user

    async def get_user_info(self, user_guid: str) -> User:
        """Retrieves user profile and online status by user GUID."""
        res = await self.execute("getUserInfo", {"user_guid": user_guid})
        return User.from_dict(res.get("data", {}).get("user", {}))

    async def get_abs_objects(self, object_guids: List[str]) -> List[Dict[str, Any]]:
        """Batch-retrieves summary objects for up to 50 GUIDs."""
        res = await self.execute("getAbsObjects", {"objects_guids": object_guids[:50]})
        return res.get("data", {}).get("abs_objects", [])

    async def get_info_by_username(self, username: str) -> Dict[str, Any]:
        """Resolves a public @username to its target entity information."""
        clean_user = username.lstrip("@")
        res = await self.execute("getObjectInfoByUsername", {"username": clean_user})
        return res.get("data", {})

    async def check_user_username(self, username: str) -> bool:
        """Checks if a username is available for an account."""
        clean_user = username.lstrip("@")
        res = await self.execute("checkUserUsername", {"username": clean_user})
        return bool(res.get("data", {}).get("is_exist") is False)

    async def update_username(self, username: str) -> Dict[str, Any]:
        """Sets or updates the account @username."""
        clean_user = username.lstrip("@")
        return await self.execute("updateUsername", {"username": clean_user})

    async def update_profile(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        bio: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Updates user first name, last name, or bio."""
        payload: Dict[str, Any] = {}
        if first_name is not None:
            payload["first_name"] = first_name
        if last_name is not None:
            payload["last_name"] = last_name
        if bio is not None:
            payload["bio"] = bio
        return await self.execute("updateProfile", payload)

    async def add_address_book(
        self,
        phone: str,
        first_name: str,
        last_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Syncs or imports a new contact into the account address book."""
        clean_phone = phone.replace("+", "").replace(" ", "").strip()
        payload = {
            "phone": clean_phone,
            "first_name": first_name,
            "last_name": last_name or "",
        }
        return await self.execute("addAddressBook", payload)

    async def get_contacts(self) -> List[User]:
        """Retrieves synced phonebook contacts."""
        res = await self.execute("getContacts", {})
        raw_users = res.get("data", {}).get("users", [])
        return [User.from_dict(u) for u in raw_users]

    async def delete_contact(self, user_guid: str) -> Dict[str, Any]:
        """Deletes a contact from the address book."""
        return await self.execute("deleteContact", {"user_guid": user_guid})

    async def block_user(self, user_guid: str) -> Dict[str, Any]:
        """Blocks a user."""
        return await self.execute(
            "setBlockUser",
            {"user_guid": user_guid, "action": "Block"},
        )

    async def unblock_user(self, user_guid: str) -> Dict[str, Any]:
        """Unblocks a previously blocked user."""
        return await self.execute(
            "setBlockUser",
            {"user_guid": user_guid, "action": "Unblock"},
        )

    async def get_blocked_users(self) -> List[User]:
        """Retrieves list of blocked users."""
        res = await self.execute("getBlockedUsers", {})
        raw_users = res.get("data", {}).get("users", [])
        return [User.from_dict(u) for u in raw_users]
