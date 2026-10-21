"""
Session management for RubiFlow.
"""

import base64
import glob
import json
import os
import re
import sqlite3
from typing import Optional

from .crypto import RubiFlowCrypto
from .exceptions import RubiFlowError


class Session:
    """Represents a RubiFlow authenticated session."""

    def __init__(
        self,
        auth: str,
        private_key_pem: str,
        dc_url: str = "https://messengerg2c332.iranlms.ir",
        user_guid: Optional[str] = None,
        phone: Optional[str] = None,
    ):
        self.auth = auth
        self.private_key_pem = private_key_pem
        self.dc_url = dc_url
        self.user_guid = user_guid
        self.phone = phone

    def to_string(self) -> str:
        """Serializes the session to a compact base64 StringSession."""
        payload = {
            "auth": self.auth,
            "key": self.private_key_pem,
            "dc": self.dc_url,
            "guid": self.user_guid,
            "phone": self.phone,
        }
        raw_json = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        return "RubiFlow$" + base64.urlsafe_b64encode(raw_json).decode("utf-8")

    @classmethod
    def from_string(cls, session_string: str) -> "Session":
        """Reconstructs a Session instance from a StringSession."""
        if not session_string.startswith("RubiFlow$"):
            raise RubiFlowError("Invalid StringSession format (missing RubiFlow$ prefix).")
        raw_b64 = session_string[len("RubiFlow$"):]
        raw_json = base64.urlsafe_b64decode(raw_b64.encode("utf-8"))
        data = json.loads(raw_json.decode("utf-8"))
        return cls(
            auth=data["auth"],
            private_key_pem=data["key"],
            dc_url=data.get("dc", "https://messengerg2c332.iranlms.ir"),
            user_guid=data.get("guid"),
            phone=data.get("phone"),
        )

    def save_to_file(self, file_path: str) -> None:
        """Saves session metadata to a local JSON file."""
        data = {
            "auth": self.auth,
            "private_key_pem": self.private_key_pem,
            "dc_url": self.dc_url,
            "user_guid": self.user_guid,
            "phone": self.phone,
        }
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @classmethod
    def load_from_file(cls, file_path: str) -> "Session":
        """Loads a session from a local JSON file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Session file not found at {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return cls(
            auth=data["auth"],
            private_key_pem=data["private_key_pem"],
            dc_url=data.get("dc_url", "https://messengerg2c332.iranlms.ir"),
            user_guid=data.get("user_guid"),
            phone=data.get("phone"),
        )

    @classmethod
    def from_firefox(cls) -> "Session":
        """
        Automatically detects and decrypts the active Rubika session from
        the user's Firefox browser profile storage.
        """
        possible_dirs = [
            os.path.expanduser("~/snap/firefox/common/.mozilla/firefox/*.default*"),
            os.path.expanduser("~/.mozilla/firefox/*.default*"),
        ]
        profile_path: Optional[str] = None
        for pattern in possible_dirs:
            matches = glob.glob(pattern)
            if matches:
                profile_path = matches[0]
                break

        if not profile_path:
            raise RubiFlowError("Could not locate Firefox default profile directory.")

        m_db_path = os.path.join(
            profile_path, "storage/default/https+++m.rubika.ir/ls/data.sqlite"
        )
        if not os.path.exists(m_db_path):
            raise RubiFlowError(
                f"No active Rubika session found in Firefox storage: {m_db_path}"
            )

        conn = sqlite3.connect(f"file:{m_db_path}?immutable=1", uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM data;")
        rows = dict(cursor.fetchall())
        conn.close()

        # Decrypt auth using m.rubika storage key
        m_storage_key = "weqrvmnxmnvljflksjlkjdsaoiuouopm"
        stored_auth = json.loads(rows["auth"].decode("utf-8"))
        raw_auth = RubiFlowCrypto.decrypt_aes(stored_auth, m_storage_key)
        if isinstance(raw_auth, dict):
            raw_auth = str(raw_auth)

        # Extract RSA key
        key_raw = rows["key"].decode("utf-8")
        if key_raw.startswith('"') and key_raw.endswith('"'):
            key_raw = json.loads(key_raw)
        key_json = json.loads(base64.b64decode(key_raw).decode("utf-8"))
        rsa_pem = key_json["d"]

        # Extract DC URL
        dcs_raw = rows.get("dcs", b"")
        dc_matches = re.findall(rb"https?://messengerg2c[0-9]+\.iranlms\.ir", dcs_raw)
        dc_url = dc_matches[0].decode() if dc_matches else "https://messengerg2c332.iranlms.ir"

        # Decrypt user profile
        user_guid = None
        phone = None
        if "profile" in rows:
            try:
                stored_profile = json.loads(rows["profile"].decode("utf-8"))
                profile_data = RubiFlowCrypto.decrypt_aes(stored_profile, raw_auth)
                if isinstance(profile_data, str):
                    profile_data = json.loads(profile_data)
                user_guid = profile_data.get("user_guid")
                phone = profile_data.get("phone")
            except Exception:
                pass

        return cls(
            auth=raw_auth,
            private_key_pem=rsa_pem,
            dc_url=dc_url,
            user_guid=user_guid,
            phone=phone,
        )
