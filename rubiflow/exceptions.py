"""
Custom exceptions for the RubiFlow framework.
"""

from typing import Optional


class RubiFlowError(Exception):
    """Base exception for all RubiFlow errors."""

    def __init__(self, message: str, status_det: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.status_det = status_det

    def __str__(self) -> str:
        if self.status_det:
            return f"{self.message} (status_det: {self.status_det})"
        return self.message


class ApiError(RubiFlowError):
    """Raised when the Rubika API returns an error status."""


class InvalidAuthError(ApiError):
    """Raised when the session authentication token is invalid or expired."""


class NetworkError(RubiFlowError):
    """Raised when a network or transport issue occurs."""


class CryptoError(RubiFlowError):
    """Raised when an encryption or decryption error occurs."""


class NotFoundError(ApiError):
    """Raised when a requested resource (user, chat, message) is not found."""


class FileError(RubiFlowError):
    """Raised when file uploading or downloading fails."""


def check_api_status(response_data: dict) -> None:
    """
    Checks the status and status_det fields of a Rubika response and raises
    the appropriate typed exception if an error is present.
    """
    status = response_data.get("status")
    status_det = response_data.get("status_det")

    if status == "OK":
        return

    if status_det == "INVALID_AUTH":
        raise InvalidAuthError(
            "The session authentication token is invalid or has expired.", status_det
        )
    elif status_det in ("NOT_FOUND", "USER_NOT_FOUND", "CHAT_NOT_FOUND"):
        raise NotFoundError(f"Requested resource was not found ({status_det}).", status_det)
    else:
        raise ApiError(f"Rubika API returned error: {status}", status_det)
