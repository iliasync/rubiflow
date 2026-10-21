"""
Authentication, 2-Step Verification, and Session management methods.
"""

from typing import Any, Dict, List, Optional


class AuthMethods:
    """Methods for login, registration, 2FA, and active sessions."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    async def send_code(
        self,
        phone_number: str,
        send_type: str = "SMS",
    ) -> Dict[str, Any]:
        """Sends an activation SMS or internal code to a phone number."""
        clean_phone = phone_number.replace("+", "").replace(" ", "").strip()
        payload = {
            "phone_number": clean_phone,
            "send_type": send_type,
        }
        return await self.execute("sendCode", payload)

    async def sign_in(
        self,
        phone_number: str,
        phone_code_hash: str,
        phone_code: str,
    ) -> Dict[str, Any]:
        """Verifies activation code and authenticates the user."""
        clean_phone = phone_number.replace("+", "").replace(" ", "").strip()
        payload = {
            "phone_number": clean_phone,
            "phone_code_hash": phone_code_hash,
            "phone_code": phone_code,
        }
        return await self.execute("signIn", payload)

    async def logout(self) -> Dict[str, Any]:
        """Logs out and invalidates the current session token."""
        return await self.execute("logout", {})

    async def register_device(
        self,
        device_model: str = "RubiFlow Framework",
        system_version: str = "Linux",
        token: str = "",
        token_type: str = "Web",
    ) -> Dict[str, Any]:
        """Registers device identification for the current account."""
        payload = {
            "app_version": "2.5.9",
            "device_hash": "RubiFlow-" + getattr(self, "session", None).auth[:8] if hasattr(self, "session") else "RubiFlow",
            "device_model": device_model,
            "is_扶_mode": False,
            "lang_code": "fa",
            "system_version": system_version,
            "token": token,
            "token_type": token_type,
        }
        return await self.execute("registerDevice", payload)

    async def get_dcs(self) -> Dict[str, Any]:
        """Fetches the list of active Data Center (DC) URLs."""
        return await self.execute("getDCs", {}, api_version="4")

    async def get_base_info(self) -> Dict[str, Any]:
        """Retrieves global platform configurations and server timestamps."""
        return await self.execute("getBaseInfo", {}, api_version="0")

    # --- Two-Step Verification (2FA) ---

    async def setup_two_step_verification(
        self,
        password: str,
        hint: Optional[str] = None,
        recovery_email: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Sets up a two-step verification password."""
        payload: Dict[str, Any] = {"password": password}
        if hint:
            payload["hint"] = hint
        if recovery_email:
            payload["recovery_email"] = recovery_email
        return await self.execute("setupTwoStepVerification", payload)

    async def check_two_step_passcode(self, password: str) -> Dict[str, Any]:
        """Validates 2FA passcode during login."""
        return await self.execute("checkTwoStepPasscode", {"password": password})

    async def change_password(
        self,
        old_password: str,
        new_password: str,
        hint: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Changes the current two-step verification password."""
        payload: Dict[str, Any] = {
            "old_password": old_password,
            "new_password": new_password,
        }
        if hint:
            payload["hint"] = hint
        return await self.execute("changePassword", payload)

    async def abort_two_step_setup(self) -> Dict[str, Any]:
        """Cancels an in-progress 2FA setup."""
        return await self.execute("abortTwoStepSetup", {})

    async def login_two_step_forget_password(self, phone_code_hash: str) -> Dict[str, Any]:
        """Requests password recovery code sent to recovery email."""
        return await self.execute("loginTwoStepForgetPassword", {"phone_code_hash": phone_code_hash})

    async def login_disable_two_step(self, phone_code_hash: str, email_code: str) -> Dict[str, Any]:
        """Disables 2FA using email confirmation code."""
        return await self.execute(
            "loginDisableTwoStep",
            {"phone_code_hash": phone_code_hash, "email_code": email_code},
        )

    async def set_recovery_email(self, email: str) -> Dict[str, Any]:
        """Sets or updates the account recovery email."""
        return await self.execute("setRecoveryEmail", {"email": email})

    async def verify_recovery_email(self, email_code: str) -> Dict[str, Any]:
        """Confirms the recovery email verification code."""
        return await self.execute("verifyRecoveryEmail", {"email_code": email_code})

    async def abort_set_recovery_email(self) -> Dict[str, Any]:
        """Aborts pending recovery email verification."""
        return await self.execute("abortSetRecoveryEmail", {})

    # --- Session Management ---

    async def get_my_sessions(self) -> List[Dict[str, Any]]:
        """Retrieves list of active logged-in sessions and devices."""
        res = await self.execute("getMySessions", {})
        return res.get("data", {}).get("sessions", [])

    async def terminate_session(self, session_key: str) -> Dict[str, Any]:
        """Terminates a specific active session by its session key."""
        return await self.execute("terminateSession", {"session_key": session_key})

    async def terminate_user_sessions(self) -> Dict[str, Any]:
        """Terminates all other logged-in sessions except the current one."""
        return await self.execute("terminateUserSessions", {})

    async def action_on_unconfirmed_session(
        self, session_key: str, action: str = "Accept"
    ) -> Dict[str, Any]:
        """Accepts or rejects an unconfirmed session login attempt."""
        return await self.execute(
            "actionOnUnconfirmedSession",
            {"session_key": session_key, "action": action},
        )
