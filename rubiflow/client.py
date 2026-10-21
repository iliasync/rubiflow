"""
Core asynchronous Client for RubiFlow.
"""

import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Union

from .crypto import RubiFlowCrypto
from .exceptions import RubiFlowError, check_api_status
from .methods import Methods
from .models import Message, User
from .network import AsyncTransport
from .session import Session

logger = logging.getLogger("rubiflow")


class Client(Methods):
    """
    High-performance, asynchronous Rubika client framework.
    Inherits 300+ methods covering Messenger, Rubino, VOD, and Wallet.
    """

    DEFAULT_DC_URL = "https://messengerg2c332.iranlms.ir"
    LIB_NAME = "RubiFlow"
    LIB_VERSION = "1.0.0"

    # Rubika protocol standard client signature
    _INTERNAL_CLIENT = {
        "app_name": "Main",
        "app_version": "2.5.9",
        "platform": "PWA",
        "package": "m.rubika.ir",
        "lang_code": "fa",
    }

    def __init__(
        self,
        session: Optional[Union[Session, str]] = None,
        auth: Optional[str] = None,
        private_key_pem: Optional[str] = None,
        dc_url: Optional[str] = None,
        timeout: float = 20.0,
    ):
        if isinstance(session, str):
            if session.startswith("RubiFlow$") or session.startswith("Rubix$"):
                self.session = Session.from_string(session)
            else:
                self.session = Session.load_from_file(session)
        elif isinstance(session, Session):
            self.session = session
        elif auth and private_key_pem:
            self.session = Session(
                auth=auth,
                private_key_pem=private_key_pem,
                dc_url=dc_url or self.DEFAULT_DC_URL,
            )
        else:
            # Temporary unauthenticated session
            priv, _ = RubiFlowCrypto.generate_rsa_key_pair()
            tmp = RubiFlowCrypto.generate_tmp_session(32)
            self.session = Session(
                auth=tmp,
                private_key_pem=priv,
                dc_url=dc_url or self.DEFAULT_DC_URL,
            )

        self.transport = AsyncTransport(timeout_seconds=timeout)
        self._me: Optional[User] = None
        self._message_handlers: List[Callable[[Message], Any]] = []
        self._is_running = False

    @classmethod
    def from_firefox(cls) -> "Client":
        """
        Creates a Client connected directly to the user's active session in Firefox.
        """
        session = Session.from_firefox()
        return cls(session=session)

    async def __aenter__(self) -> "Client":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.stop()

    async def start(self) -> None:
        """Initializes client and verifies session authentication."""
        try:
            me = await self.get_me()
            self._me = me
            logger.info("RubiFlow connected as @%s (%s)", me.username, me.guid)
        except Exception as exc:
            logger.warning("RubiFlow started with unverified session: %s", exc)

    async def stop(self) -> None:
        """Closes transport and background tasks."""
        self._is_running = False
        await self.transport.close()

    # --- Core RPC Dispatcher ---

    async def execute(
        self,
        method: str,
        input_data: Optional[Dict[str, Any]] = None,
        api_version: str = "6",
    ) -> Dict[str, Any]:
        """
        Executes an encrypted and RSA-signed Rubika V6 RPC method.
        """
        inner_payload = {
            "method": method,
            "input": input_data or {},
            "client": self._INTERNAL_CLIENT,
        }

        # 1. AES encrypt inner payload with derived secret
        data_enc = RubiFlowCrypto.encrypt_aes(inner_payload, self.session.auth)

        # 2. RSA-SHA256 signature
        sign = RubiFlowCrypto.sign_rsa_sha256(data_enc, self.session.private_key_pem)

        # 3. Disguise auth token
        disguised_auth = RubiFlowCrypto.disguise_auth(self.session.auth)

        request_body = {
            "api_version": api_version,
            "auth": disguised_auth,
            "data_enc": data_enc,
            "sign": sign,
        }

        response = await self.transport.post_json(self.session.dc_url, request_body)

        if "data_enc" in response:
            decrypted = RubiFlowCrypto.decrypt_aes(response["data_enc"], self.session.auth)
            if isinstance(decrypted, str):
                decrypted = json.loads(decrypted)
            check_api_status(decrypted)
            return decrypted

        check_api_status(response)
        return response

    async def invoke(self, method: str, **kwargs) -> Dict[str, Any]:
        """
        Directly invokes any Rubika RPC method with arbitrary input arguments.
        Example: await app.invoke('sendMessage', object_guid='u0...', text='Hello')
        """
        return await self.execute(method, kwargs)

    # --- Event Handling & Bot Loop ---

    def on_message(self) -> Callable[[Callable[[Message], Any]], Callable[[Message], Any]]:
        """Decorator to register an asynchronous handler for incoming messages."""
        def decorator(func: Callable[[Message], Any]) -> Callable[[Message], Any]:
            self._message_handlers.append(func)
            return func
        return decorator

    async def _polling_loop(self) -> None:
        """Background poller for message updates."""
        while self._is_running:
            try:
                chats = await self.get_chats()
                for chat in chats:
                    if chat.unread_count > 0:
                        msgs = await self.get_messages(chat.guid, limit=chat.unread_count)
                        for msg in msgs:
                            for handler in self._message_handlers:
                                if asyncio.iscoroutinefunction(handler):
                                    await handler(msg)
                                else:
                                    handler(msg)
                await asyncio.sleep(2)
            except Exception as exc:
                logger.error("Polling error: %s", exc)
                await asyncio.sleep(5)

    def run(self, coro: Optional[Any] = None) -> None:
        """
        Convenience runner for scripts and bot processes.
        """
        loop = asyncio.get_event_loop()
        if coro is not None:
            loop.run_until_complete(coro)
            return

        async def _main():
            async with self:
                self._is_running = True
                await self._polling_loop()

        try:
            loop.run_until_complete(_main())
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            loop.run_until_complete(self.stop())
