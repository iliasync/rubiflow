"""
Cryptographic engine for RubiFlow (Rubika V6 Protocol).
Implements AES-256-CBC, custom key derivation, substitution auth disguising,
and RSA-SHA256 asymmetric signatures.
"""

import base64
import json
import random
import string
from typing import Any, Dict, Union

from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
    load_pem_private_key,
)

from .exceptions import CryptoError


class RubiFlowCrypto:
    """Cryptographic operations required by the Rubika V6 protocol."""

    STATIC_IV = b"\x00" * 16

    @staticmethod
    def generate_rsa_key_pair() -> tuple[str, str]:
        """
        Generates a new 1024-bit RSA key pair in PEM format.
        Returns: (private_key_pem, public_key_pem)
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1024,
        )
        private_pem = private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption(),
        ).decode("utf-8")

        public_pem = private_key.public_key().public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

        return private_pem, public_pem

    @staticmethod
    def generate_tmp_session(length: int = 32) -> str:
        """Generates a random lowercase ASCII string for unauthenticated sessions."""
        return "".join(random.choices(string.ascii_lowercase, k=length))

    @staticmethod
    def create_secret_passphrase(auth: str) -> str:
        """
        Derives the 32-character AES secret key from an auth token or tmp_session.
        """
        if len(auth) < 32:
            raise CryptoError("Auth key or tmp_session must have at least 32 characters.")

        t = auth[0:8]
        i = auth[8:16]
        p1 = auth[16:24]
        p2 = auth[24:32]

        chars = list(p1 + t + p2 + i)
        for idx, char in enumerate(chars):
            if "0" <= char <= "9":
                chars[idx] = chr((ord(char) - ord("0") + 5) % 10 + ord("0"))
            elif "a" <= char <= "z":
                chars[idx] = chr((ord(char) - ord("a") + 9) % 26 + ord("a"))

        return "".join(chars)

    @staticmethod
    def disguise_auth(auth: str) -> str:
        """
        Applies the Rubika V6 character substitution cipher to the auth string.
        """
        result = []
        for char in auth:
            if "0" <= char <= "9":
                result.append(chr((13 + (ord(char) - ord("0"))) % 10 + ord("0")))
            elif "A" <= char <= "Z":
                result.append(chr((29 - (ord(char) - ord("A"))) % 26 + ord("A")))
            elif "a" <= char <= "z":
                result.append(chr((32 - (ord(char) - ord("a"))) % 26 + ord("a")))
            else:
                result.append(char)
        return "".join(result)

    @classmethod
    def encrypt_aes(cls, data: Union[Dict[str, Any], str], auth: str) -> str:
        """
        Encrypts a dictionary or string payload using AES-256-CBC and returns Base64.
        """
        try:
            passphrase = cls.create_secret_passphrase(auth).encode("utf-8")
            if isinstance(data, dict):
                raw_bytes = json.dumps(
                    data, separators=(",", ":"), ensure_ascii=False
                ).encode("utf-8")
            else:
                raw_bytes = data.encode("utf-8")

            padder = padding.PKCS7(128).padder()
            padded = padder.update(raw_bytes) + padder.finalize()

            cipher = Cipher(algorithms.AES(passphrase), modes.CBC(cls.STATIC_IV))
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded) + encryptor.finalize()

            return base64.b64encode(ciphertext).decode("utf-8")
        except Exception as exc:
            raise CryptoError(f"AES encryption failed: {exc}") from exc

    @classmethod
    def decrypt_aes(cls, encrypted_b64: str, auth: str) -> Union[Dict[str, Any], str]:
        """
        Decrypts a Base64 AES-256-CBC ciphertext and parses it as JSON if possible.
        """
        try:
            passphrase = cls.create_secret_passphrase(auth).encode("utf-8")
            raw_ciphertext = base64.b64decode(encrypted_b64)

            cipher = Cipher(algorithms.AES(passphrase), modes.CBC(cls.STATIC_IV))
            decryptor = cipher.decryptor()
            padded_plain = decryptor.update(raw_ciphertext) + decryptor.finalize()

            unpadder = padding.PKCS7(128).unpadder()
            plain_bytes = unpadder.update(padded_plain) + unpadder.finalize()
            plain_text = plain_bytes.decode("utf-8")

            try:
                return json.loads(plain_text)
            except json.JSONDecodeError:
                return plain_text
        except Exception as exc:
            raise CryptoError(f"AES decryption failed: {exc}") from exc

    @staticmethod
    def sign_rsa_sha256(data_enc_b64: str, private_key_pem: str) -> str:
        """
        Signs the data_enc string using RSA-SHA256 with the client's private key.
        Returns the Base64-encoded signature.
        """
        try:
            pem_bytes = (
                private_key_pem.encode("utf-8")
                if isinstance(private_key_pem, str)
                else private_key_pem
            )
            private_key = load_pem_private_key(pem_bytes, password=None)
            signature = private_key.sign(
                data_enc_b64.encode("utf-8"),
                asym_padding.PKCS1v15(),
                hashes.SHA256(),
            )
            return base64.b64encode(signature).decode("utf-8")
        except Exception as exc:
            raise CryptoError(f"RSA signature failed: {exc}") from exc
