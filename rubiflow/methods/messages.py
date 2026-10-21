"""
Messages, Reactions, Polls, Drafts, and Pinned message methods.
"""

import random
from typing import Any, Dict, List, Optional, Union

from ..models import Message


class MessagesMethods:
    """Methods for message creation, manipulation, reactions, and polling."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    async def send_message(
        self,
        target: str,
        text: str,
        reply_to_message_id: Optional[str] = None,
    ) -> Message:
        """Sends a text message to a user, group, or channel."""
        rnd = random.randint(100000, 999999999)
        payload: Dict[str, Any] = {
            "object_guid": target,
            "rnd": rnd,
            "text": text,
        }
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)

        res = await self.execute("sendMessage", payload)
        msg_dict = res.get("data", {}).get("message_update", {})
        return Message.from_dict(msg_dict, client=self)

    async def edit_message(
        self,
        target: str,
        message_id: str,
        text: str,
    ) -> Message:
        """Edits an existing message."""
        payload = {
            "object_guid": target,
            "message_id": str(message_id),
            "text": text,
        }
        res = await self.execute("editMessage", payload)
        return Message.from_dict(res.get("data", {}).get("message_update", {}), client=self)

    async def delete_messages(
        self,
        target: str,
        message_ids: List[Union[str, int]],
        delete_for_all: bool = True,
    ) -> Dict[str, Any]:
        """Deletes one or multiple messages."""
        payload = {
            "object_guid": target,
            "message_ids": [str(m) for m in message_ids],
            "type": "Global" if delete_for_all else "Local",
        }
        return await self.execute("deleteMessages", payload)

    async def forward_messages(
        self,
        from_target: str,
        to_target: str,
        message_ids: List[Union[str, int]],
    ) -> Dict[str, Any]:
        """Forwards messages between dialogs."""
        rnd = random.randint(100000, 999999999)
        payload = {
            "from_object_guid": from_target,
            "to_object_guid": to_target,
            "message_ids": [str(m) for m in message_ids],
            "rnd": rnd,
        }
        return await self.execute("forwardMessages", payload)

    async def get_messages(
        self,
        target: str,
        limit: int = 30,
        middle_message_id: Optional[Union[str, int]] = None,
        filter_type: Optional[str] = None,
    ) -> List[Message]:
        """
        Retrieves message history of a chat.
        Resolves latest message id automatically if omitted.
        """
        if middle_message_id is None:
            chats = await self.get_chats()
            for c in chats:
                if c.guid == target and c.last_message_id:
                    middle_message_id = c.last_message_id
                    break

        payload: Dict[str, Any] = {"object_guid": target}
        if middle_message_id is not None:
            payload["middle_message_id"] = str(middle_message_id)
        if filter_type:
            payload["filter_type"] = filter_type

        res = await self.execute("getMessagesInterval", payload)
        raw_msgs = res.get("data", {}).get("messages", [])
        return [Message.from_dict(m, client=self) for m in raw_msgs][:limit]

    async def get_messages_by_id(
        self,
        target: str,
        message_ids: List[Union[str, int]],
    ) -> List[Message]:
        """Fetches messages by their specific message IDs."""
        payload = {
            "object_guid": target,
            "message_ids": [str(m) for m in message_ids],
        }
        res = await self.execute("getMessagesByID", payload)
        raw_msgs = res.get("data", {}).get("messages", [])
        return [Message.from_dict(m, client=self) for m in raw_msgs]

    async def get_messages_updates(self, target: str, state: int) -> Dict[str, Any]:
        """Retrieves new message updates since a sync state sequence."""
        return await self.execute("getMessagesUpdates", {"object_guid": target, "state": state})

    async def search_chat_messages(
        self,
        target: str,
        search_text: str,
    ) -> List[Message]:
        """Searches messages inside a specific chat."""
        payload = {
            "object_guid": target,
            "search_text": search_text,
        }
        res = await self.execute("searchChatMessages", payload)
        raw_msgs = res.get("data", {}).get("messages", [])
        return [Message.from_dict(m, client=self) for m in raw_msgs]

    async def search_global_messages(
        self,
        search_text: str,
    ) -> List[Message]:
        """Searches messages globally across all joined chats."""
        res = await self.execute("searchGlobalMessages", {"search_text": search_text})
        raw_msgs = res.get("data", {}).get("messages", [])
        return [Message.from_dict(m, client=self) for m in raw_msgs]

    async def send_chat_activity(
        self,
        target: str,
        activity: str = "Typing",
    ) -> Dict[str, Any]:
        """
        Sends typing or action indicator.
        Allowed activity values: 'Typing', 'Recording', 'Uploading'
        """
        return await self.execute(
            "sendChatActivity",
            {"object_guid": target, "activity": activity},
        )

    # --- Reactions & Pinned Messages ---

    async def action_on_message_reaction(
        self,
        target: str,
        message_id: Union[str, int],
        reaction_id: int,
        action: str = "Add",
    ) -> Dict[str, Any]:
        """Adds or removes a reaction emoji on a message."""
        payload = {
            "object_guid": target,
            "message_id": str(message_id),
            "reaction_id": reaction_id,
            "action": action,
        }
        return await self.execute("actionOnMessageReaction", payload)

    async def get_message_reactions(
        self,
        target: str,
        message_id: Union[str, int],
    ) -> Dict[str, Any]:
        """Fetches reaction details and voter breakdown for a message."""
        return await self.execute(
            "getMessageReactions",
            {"object_guid": target, "message_id": str(message_id)},
        )

    async def get_available_reactions(self) -> List[Dict[str, Any]]:
        """Retrieves list of all available reaction emojis."""
        res = await self.execute("getAvailableReactions", {})
        return res.get("data", {}).get("reactions", [])

    async def get_message_share_url(
        self,
        target: str,
        message_id: Union[str, int],
    ) -> str:
        """Generates public share URL for a message."""
        res = await self.execute(
            "getMessageShareUrl",
            {"object_guid": target, "message_id": str(message_id)},
        )
        return res.get("data", {}).get("share_url", "")

    async def pin_chat_message(
        self,
        target: str,
        message_id: Union[str, int],
        notify_members: bool = True,
    ) -> Dict[str, Any]:
        """Pins a message at the top of a group or channel."""
        payload = {
            "object_guid": target,
            "message_id": str(message_id),
            "action": "Pin",
            "notify": notify_members,
        }
        return await self.execute("setPinMessage", payload)

    async def unpin_chat_message(
        self,
        target: str,
        message_id: Union[str, int],
    ) -> Dict[str, Any]:
        """Unpins a previously pinned message."""
        payload = {
            "object_guid": target,
            "message_id": str(message_id),
            "action": "Unpin",
        }
        return await self.execute("setPinMessage", payload)

    async def get_pin_message_history(self, target: str) -> List[Message]:
        """Retrieves list of all pinned messages in a conversation."""
        res = await self.execute("getPinMessageHistory", {"object_guid": target})
        raw_msgs = res.get("data", {}).get("messages", [])
        return [Message.from_dict(m, client=self) for m in raw_msgs]

    # --- Polls ---

    async def create_poll(
        self,
        target: str,
        question: str,
        options: List[str],
        is_anonymous: bool = True,
        allows_multiple_answers: bool = False,
    ) -> Dict[str, Any]:
        """Creates a poll in a chat."""
        rnd = random.randint(100000, 999999999)
        payload = {
            "object_guid": target,
            "question": question,
            "options": options,
            "is_anonymous": is_anonymous,
            "allows_multiple_answers": allows_multiple_answers,
            "rnd": rnd,
        }
        return await self.execute("createPoll", payload)

    async def vote_poll(
        self,
        target: str,
        poll_id: str,
        selection_index: int,
    ) -> Dict[str, Any]:
        """Votes on a poll option."""
        payload = {
            "object_guid": target,
            "poll_id": poll_id,
            "selection_index": selection_index,
        }
        return await self.execute("votePoll", payload)

    async def get_poll_results(self, target: str, poll_id: str) -> Dict[str, Any]:
        """Fetches current vote counts and breakdown of a poll."""
        return await self.execute("getPollResults", {"object_guid": target, "poll_id": poll_id})

    # --- Drafts & Inline Links ---

    async def get_all_drafts(self) -> List[Dict[str, Any]]:
        """Retrieves all unsent text drafts saved across devices."""
        res = await self.execute("getAllDrafts", {})
        return res.get("data", {}).get("drafts", [])

    async def update_draft(
        self,
        target: str,
        text: str,
        reply_to_message_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Saves a draft message for a chat."""
        payload: Dict[str, Any] = {
            "object_guid": target,
            "draft_text": text,
        }
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)
        return await self.execute("updateDraft", payload)

    async def clear_drafts(self, target: str) -> Dict[str, Any]:
        """Clears draft for a conversation."""
        return await self.execute("clearDrafts", {"object_guid": target})

    async def click_message_url(self, link_url: str) -> Dict[str, Any]:
        """Resolves an inline short URL in messages."""
        return await self.execute("clickMessageUrl", {"url": link_url})
