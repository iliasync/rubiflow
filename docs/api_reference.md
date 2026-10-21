# 📚 RubiFlow API Reference

Welcome to the **RubiFlow API Reference**. This documentation follows the structure and style of the official [Telegram Bot API](https://core.telegram.org/bots/api), presenting every method with input parameters, types, required flags, return structures, and ready-to-run asynchronous Python code samples.

---

## Architecture Overview

All methods are exposed directly through the high-level `rubiflow.Client` class via modular Python mixins:

```
                            ┌─────────────────────┐
                            │   rubiflow.Client   │
                            └──────────┬──────────┘
       ┌───────────────────────────────┼───────────────────────────────┐
       │                               │                               │
┌──────▼────────┐              ┌───────▼────────┐              ┌───────▼────────┐
│MessagesMethods│              │  ChatsMethods  │              │ GroupsMethods  │
└───────────────┘              └────────────────┘              └────────────────┘
       │                               │                               │
┌──────▼────────┐              ┌───────▼────────┐              ┌───────▼────────┐
│ChannelsMethods│              │  UsersMethods  │              │  FilesMethods  │
└───────────────┘              └────────────────┘              └────────────────┘
       │                               │                               │
┌──────▼────────┐              ┌───────▼────────┐              ┌───────▼────────┐
│FoldersMethods │              │SettingsMethods │              │ RubinoMethods  │
└───────────────┘              └────────────────┘              └────────────────┘
       │                               │                               │
┌──────▼────────┐              ┌───────▼────────┐              ┌───────▼────────┐
│  VodMethods   │              │ WalletMethods  │              │  AuthMethods   │
└───────────────┘              └────────────────┘              └────────────────┘
```

---

## Navigation & Categories

| Category | Description | Methods Count |
| :--- | :--- | :--- |
| [Messaging & Polls](methods_messages.md) | Sending, editing, deleting, forwarding, searching messages, pinning, and interactive polls. | 13 methods |
| [Chats & Dialogs](methods_chats.md) | Dialog list retrieval, unread indicators, chat metadata, and clearing history. | 5 methods |
| [Groups & Voice Chats](methods_groups.md) | Supergroup management, member roles, bans, default permissions, and WebRTC voice chats. | 11 methods |
| [Channels & Broadcasts](methods_channels.md) | Channel creation, subscribers, admin permissions, and public username management. | 9 methods |
| [Users & Contacts](methods_users.md) | Profile inspection, blocking/unblocking, address book contacts, and @username reservation. | 11 methods |
| [Cloud Files & CDN](methods_files.md) | Uploading, downloading, chunked streaming across Rubika CDN nodes, and sticker packs. | 5 methods |
| [Folders & Organization](methods_folders.md) | Custom dialog folders and filter rules (Personal, Groups, Channels, Bots). | 3 methods |
| [Settings & Privacy](methods_settings.md) | Profile visibility, two-step verification, appearance themes, and active session termination. | 8 methods |
| [Rubino Social Network](methods_rubino.md) | Instagram-style social network: feed explore, likes, comments, stories, and following. | 16 methods |
| [VOD Movies & Series](methods_vod.md) | Rubika streaming video: HLS playlists, filmography, watchlists, and search. | 9 methods |
| [Wallet & Payments](methods_wallet.md) | In-app credit, transaction history, balance queries, and user-to-user transfers. | 4 methods |
| [Universal Invoker](methods_invoker.md) | Execute any of the **301 reverse-engineered RPC methods** directly with custom payloads. | 301 methods |

---

## Standard Response Format

RubiFlow returns either typed model instances (such as `Message`, `Chat`, or `User`) or dictionary responses mirroring the server JSON. 

When invoking lower-level methods, the response dictionary follows this structure:

```json
{
  "status": "OK",
  "status_code": 200,
  "data": {
    "message_id": "1234567890",
    "chat_guid": "u0ABCDEF1234567890"
  }
}
```

If an error occurs, RubiFlow raises `RubikaRPCError` or `RubikaNetworkError` containing the server error code (e.g., `ERROR_GENERIC`, `TOO_MANY_REQUESTS`, `ACCESS_DENIED`).
