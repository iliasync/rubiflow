"""
Unified Methods Mixin combining all specialized API submodules.
"""

from .auth import AuthMethods
from .channels import ChannelsMethods
from .chats import ChatsMethods
from .files import FilesMethods
from .folders import FoldersMethods
from .groups import GroupsMethods
from .messages import MessagesMethods
from .rubino import RubinoMethods
from .settings import SettingsMethods
from .users import UsersMethods
from .vod import VodMethods
from .wallet import WalletMethods


class Methods(
    AuthMethods,
    MessagesMethods,
    ChatsMethods,
    GroupsMethods,
    ChannelsMethods,
    UsersMethods,
    FilesMethods,
    FoldersMethods,
    SettingsMethods,
    RubinoMethods,
    VodMethods,
    WalletMethods,
):
    """
    Combined Mixin providing direct access to 300+ Rubika RPC methods.
    """


__all__ = [
    "Methods",
    "AuthMethods",
    "MessagesMethods",
    "ChatsMethods",
    "GroupsMethods",
    "ChannelsMethods",
    "UsersMethods",
    "FilesMethods",
    "FoldersMethods",
    "SettingsMethods",
    "RubinoMethods",
    "VodMethods",
    "WalletMethods",
]
