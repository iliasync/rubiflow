"""
Core asynchronous Client for RubiFlow.
"""

import asyncio
import json
import logging
import os
import re
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
    DEFAULT_SESSION_NAME = "rubiflow"
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
        session_name: Optional[str] = None,
        auth: Optional[str] = None,
        private_key_pem: Optional[str] = None,
        dc_url: Optional[str] = None,
        timeout: float = 20.0,
        interactive: bool = True,
    ):
        self._interactive = interactive
        self._default_dc_url = dc_url or self.DEFAULT_DC_URL

        # Determine target session identifier
        # Client("my_bot") sets session="my_bot"
        # Client(session_name="my_bot") sets session_name="my_bot"
        sess_target = session_name if session_name is not None else session

        if isinstance(session, Session):
            self.session = session
        elif isinstance(sess_target, str) and (sess_target.startswith("RubiFlow$") or sess_target.startswith("Rubix$")):
            self.session = Session.from_string(sess_target)
        elif sess_target == ":memory:":
            self.session = Session.new_temporary(dc_url=self._default_dc_url)
        elif auth and private_key_pem:
            self.session = Session(
                auth=auth,
                private_key_pem=private_key_pem,
                dc_url=self._default_dc_url,
                is_authenticated=True,
            )
        else:
            # File-based session (default: "rubiflow.session")
            if not sess_target:
                file_path = f"{self.DEFAULT_SESSION_NAME}.session"
            elif isinstance(sess_target, str):
                if sess_target.endswith((".session", ".rubiflow", ".json")):
                    file_path = sess_target
                else:
                    file_path = f"{sess_target}.session"
            else:
                file_path = f"{self.DEFAULT_SESSION_NAME}.session"

            if os.path.exists(file_path):
                try:
                    self.session = Session.load_from_file(file_path)
                    logger.info("Loaded existing session from '%s'", file_path)
                except Exception as exc:
                    logger.warning("Could not load session from '%s' (%s). Creating new session.", file_path, exc)
                    self.session = Session.new_temporary(file_path=file_path, dc_url=self._default_dc_url)
            else:
                self.session = Session.new_temporary(file_path=file_path, dc_url=self._default_dc_url)

        self.transport = AsyncTransport(timeout_seconds=timeout)
        self._me: Optional[User] = None
        self._message_handlers: List[Callable[[Message], Any]] = []
        self._is_running = False

    @classmethod
    def from_firefox(cls, session_name: Optional[str] = None) -> "Client":
        """
        Creates a Client connected directly to the user's active session in Firefox.
        Optionally persists the session to a session file name.
        """
        session = Session.from_firefox()
        if session_name:
            file_path = session_name if session_name.endswith((".session", ".rubiflow", ".json")) else f"{session_name}.session"
            session.file_path = file_path
            session.save()
        return cls(session=session)

    @staticmethod
    def _clean_phone_number(phone: str) -> str:
        """Normalizes phone numbers to standard format."""
        cleaned = re.sub(r"[^\d]", "", phone)
        if cleaned.startswith("0098"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("09") and len(cleaned) == 11:
            cleaned = "98" + cleaned[1:]
        elif cleaned.startswith("9") and len(cleaned) == 10:
            cleaned = "98" + cleaned
        return cleaned

    @staticmethod
    async def _async_input(prompt_text: str) -> str:
        """Prompts for input asynchronously without blocking the event loop."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: input(prompt_text).strip())

    @staticmethod
    async def _async_password(prompt_text: str) -> str:
        """Prompts for hidden password input asynchronously."""
        import getpass
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: getpass.getpass(prompt_text).strip())

    async def interactive_login(self, phone: Optional[str] = None) -> User:
        """
        Performs interactive terminal login (phone number, activation SMS code,
        and 2-Step Verification password) and automatically saves the session file.
        """
        session_label = self.session.file_path or "In-Memory Session"
        print("\n" + "=" * 60)
        print("              ⚡ RubiFlow Interactive Login ⚡")
        print("=" * 60)
        print(f"[*] Session File : {session_label}")
        print("-" * 60)

        # 1. Ask for phone number if not supplied
        while not phone:
            raw_phone = await self._async_input("[?] Enter phone number (+98... or 09...): ")
            cleaned = self._clean_phone_number(raw_phone)
            if len(cleaned) >= 10:
                phone = cleaned
                break
            print("[!] Invalid phone number format. Please try again.")

        clean_phone = self._clean_phone_number(phone)
        print(f"[*] Requesting activation code for +{clean_phone}...")

        code_res = await self.send_code(clean_phone)
        code_data = code_res.get("data", {})
        phone_code_hash = code_data.get("phone_code_hash")

        if not phone_code_hash:
            raise RubiFlowError(f"Failed to obtain phone_code_hash from Rubika: {code_res}")

        print("[+] Activation code sent via SMS / Rubika application!")

        # 2. Activation Code (with retries)
        sign_data: Dict[str, Any] = {}
        max_attempts = 3
        for attempt in range(max_attempts):
            sms_code = await self._async_input("[?] Enter the activation code: ")
            if not sms_code:
                continue
            print("[*] Verifying activation code...")
            try:
                sign_res = await self.sign_in(clean_phone, phone_code_hash, sms_code)
                sign_data = sign_res.get("data", {})
                break
            except Exception as exc:
                print(f"[!] Code verification error: {exc}")
                if attempt < max_attempts - 1:
                    print(f"[*] Attempts remaining: {max_attempts - 1 - attempt}. Try again.")
                else:
                    raise

        status = sign_data.get("status", "")
        two_step = sign_data.get("two_step_status")
        auth_token = sign_data.get("auth")

        # 3. Two-Step Verification (2FA) if required
        if status in ("TwoStepRequired", "NeedTwoPass", "TwoStepPasscode") or two_step == "Enabled" or (not auth_token and "hint" in sign_data):
            hint = sign_data.get("hint")
            print("\n[!] Two-Step Verification (2FA) is enabled on this account.")
            if hint:
                print(f"[i] Password Hint: {hint}")

            for attempt in range(max_attempts):
                password = await self._async_password("[?] Enter your 2FA password: ")
                print("[*] Validating 2FA password...")
                try:
                    pass_res = await self.check_two_step_passcode(password)
                    pass_data = pass_res.get("data", {})
                    auth_token = pass_data.get("auth") or pass_res.get("auth")
                    if auth_token:
                        sign_data = pass_data
                        break
                except Exception as exc:
                    print(f"[!] 2FA verification error: {exc}")
                    if attempt < max_attempts - 1:
                        print(f"[*] Attempts remaining: {max_attempts - 1 - attempt}. Try again.")
                    else:
                        raise

        auth_token = sign_data.get("auth") or auth_token
        if not auth_token:
            raise RubiFlowError(f"Login failed: no auth token received from server: {sign_data}")

        # Update active session with server credentials
        user_info = sign_data.get("user", {})
        self.session.auth = auth_token
        self.session.user_guid = user_info.get("user_guid")
        self.session.phone = clean_phone
        self.session.is_authenticated = True

        # Register device identity
        try:
            await self.register_device(
                device_model="RubiFlow Framework",
                system_version="Linux (RubiFlow)",
            )
        except Exception as exc:
            logger.debug("Device registration note: %s", exc)

        # Save session file
        if self.session.file_path:
            self.session.save()
            print(f"[+] Session saved successfully to: {self.session.file_path}")

        # Fetch profile
        me = await self.get_me()
        self._me = me
        print(f"[+] Successfully logged in as: {me.full_name} (@{me.username})")
        print("=" * 60 + "\n")
        return me

    async def __aenter__(self) -> "Client":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.stop()

    async def start(self) -> None:
        """Initializes client and verifies session authentication."""
        if not self.session.is_authenticated:
            if self._interactive:
                await self.interactive_login()
            else:
                raise RubiFlowError(
                    f"Session '{self.session.file_path or 'unnamed'}' is not authenticated and interactive login is disabled."
                )
        else:
            try:
                me = await self.get_me()
                self._me = me
                logger.info("RubiFlow connected as @%s (%s)", me.username, me.guid)
            except Exception as exc:
                logger.warning("Session verification failed: %s", exc)
                if self._interactive:
                    print(f"\n[!] Session verification failed ({exc}).")
                    print("[!] Starting interactive login to renew authentication...")
                    await self.interactive_login()
                else:
                    raise

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
