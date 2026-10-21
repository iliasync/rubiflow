# Complete Rubika API Methods Catalog

This catalog contains all methods extracted from `web.rubika.ir` (Angular Messenger Web client - 203 RPC methods) and `m.rubika.ir` (React SuperApp / PWA client - 111 methods across Rubino, VOD, Wallet, and Messenger V6).

---

## 1. Web Client Methods (`web.rubika.ir`) - Messenger Core (203 Methods)

### 1.1 Authentication, Login & Security
- `sendCode`: Send SMS / in-app verification code for login.
- `signIn`: Submit activation code and establish session.
- `logout`: Invalidate current auth session.
- `registerDevice`: Register client app details and push token.
- `getDCs`: Retrieve available Data Center endpoints (`messengerg2c*.iranlms.ir`).
- `getBaseInfo`: Retrieve platform configuration, limits, and server time.
- `setupTwoStepVerification`: Enable 2-step verification password.
- `checkTwoStepPasscode`: Validate 2-step verification password upon login.
- `changePassword`: Change 2-step verification password.
- `abortTwoStepSetup`: Abort in-progress 2FA setup.
- `loginTwoStepForgetPassword`: Request password reset via recovery email.
- `loginDisableTwoStep`: Disable 2FA via email recovery code.
- `setRecoveryEmail`: Set or update account recovery email.
- `verifyRecoveryEmail`: Confirm recovery email with code.
- `abortSetRecoveryEmail`: Cancel pending recovery email setup.
- `terminateUserSessions`: Terminate other active sessions.
- `terminateSession`: Terminate a specific device session by ID.
- `getMySessions`: List all logged-in devices and IP sessions.
- `actionOnUnconfirmedSession`: Approve or reject new login attempts.

### 1.2 Chats & Messaging
- `sendMessage`: Send a text or media message to user/group/channel.
- `editMessage`: Edit message text or formatting.
- `deleteMessages`: Delete one or multiple messages (for self or everyone).
- `forwardMessages`: Forward messages to target chat.
- `getMessages`: Retrieve message history by message IDs.
- `getMessagesInterval`: Retrieve paginated messages (before/after message ID).
- `getMessagesUpdates`: Stream message updates and delivery receipts.
- `getChats`: Paginated list of dialogs/chats.
- `getChatsUpdates`: Real-time updates for chat list.
- `getTopChatList`: Frequently contacted chats.
- `searchChatMessages`: Search text within a chat history.
- `searchGlobalMessages`: Search text across all joined chats.
- `searchChats`: Search chat titles and usernames.
- `deleteChatHistory`: Clear all messages in a conversation.
- `deleteUserChat`: Delete a direct 1-to-1 conversation.
- `deleteGroupChat` / `deleteNoAccessGroupChat`: Leave and delete group chat.
- `deleteChannelChat`: Leave and delete channel.
- `actionOnMessageReaction`: Add or remove emoji reaction on a message.
- `getAvailableReactions`: List available emoji reactions for messages.
- `getMessageReactionDetail`: List users who reacted with specific emojis.
- `sendChatActivity`: Send typing / recording audio / uploading media indicators.
- `seenChats`: Mark messages as read / update read receipt.
- `pinChatMessage`: Pin a message in group/channel.
- `unpinChatMessage`: Unpin a message.
- `getPinMessageHistory`: List all pinned messages.
- `clickMessageUrl`: Resolve and log inline links.
- `createPoll`: Create a vote poll.
- `votePoll`: Cast a vote on a poll.
- `getPollResults`: Retrieve poll options and voter breakdown.

### 1.3 Groups & Supergroups
- `addGroup`: Create a new group.
- `getGroupInfo`: Get group metadata, title, avatar, description.
- `editGroupInfo`: Update group title, description, or permissions.
- `getGroupMembers`: Paginated list of group members.
- `addGroupMembers`: Add users to group.
- `banGroupMember`: Remove and ban user from group.
- `setGroupAdmin`: Promote member to group admin with custom permissions.
- `setGroupDefaultAccess`: Configure member default permissions (send text, media, etc.).
- `getGroupDefaultAccess`: Fetch group permissions config.
- `getGroupAdminMembers`: List all administrators.
- `leaveGroup`: Exit group.
- `getGroupAdminAccessList`: List granted permissions for an admin.
- `createGroupVoiceChat`: Start group live audio space.
- `discardGroupVoiceChat`: End live audio space.
- `joinGroupVoiceChat`: Join active voice room.
- `getGroupVoiceChat`: Get voice chat participants and SDP info.

### 1.4 Channels
- `addChannel`: Create a new channel.
- `getChannelInfo`: Channel title, bio, subscriber count.
- `editChannelInfo`: Edit channel metadata and settings.
- `getChannelMembers`: List channel subscribers.
- `addChannelMembers`: Add contacts to channel.
- `banChannelMember`: Ban subscriber from channel.
- `setChannelAdmin`: Add/edit channel administrators.
- `getChannelAdminMembers`: List channel admins.
- `channelPreviewByJoinLink`: Fetch public preview of channel via invite link.
- `createJoinLink`: Generate invite link with custom expiration and usage limits.
- `editJoinLink`: Modify invite link settings.
- `deleteRevokedJoinLink`: Invalidate invite links.
- `actionOnJoinRequest`: Accept or decline pending join requests.
- `checkChannelUsername`: Verify if a channel @username is available.
- `updateChannelUsername`: Assign public username to channel.

### 1.5 File Storage & Media CDN
- `requestSendFile`: Request upload endpoint, token, and DC for a file.
- `uploadFile`: Post file chunks to assigned CDN storage node.
- `getFile`: Download file payload/stream.
- `getAvatars`: Fetch profile photos and avatars history.
- `uploadAvatar`: Upload new avatar for user, group, or channel.
- `deleteAvatar`: Delete avatar photo.

### 1.6 Contacts, Profiles & Users
- `getUserInfo`: Get user profile, bio, online status, username.
- `getAbsObjects`: Batch-fetch metadata for multiple GUIDs (users, groups, channels).
- `checkUserUsername`: Check availability of user @username.
- `updateUsername`: Change user public username.
- `updateProfile`: Change first name, last name, bio.
- `addAddressBook`: Sync phonebook contacts.
- `getContacts`: Get synced contacts list.
- `deleteContact`: Remove user from contacts.
- `blockUser` / `setBlock`: Block user.
- `unblockUser`: Unblock user.
- `getBlockedUsers`: List blocked accounts.

### 1.7 Folders & Drafts
- `addFolder`: Create custom chat folder/tab.
- `editFolder`: Update folder name and included/excluded chats.
- `deleteFolder`: Remove chat folder.
- `getFolders`: Retrieve all user chat folders.
- `getAllDrafts`: Synchronize unsent text drafts across devices.
- `updateDraft`: Save draft for a chat.
- `clearDrafts`: Discard draft.

### 1.8 Settings & Appearance
- `getAppearanceSetting` / `setAppearanceSetting`: Themes, font sizes, bubble styles.
- `getPrivacySetting` / `setPrivacySetting`: Last seen, profile picture, phone number visibility.
- `getNotificationSetting` / `setNotificationSetting`: Sound, vibration, mute exceptions.
- `getStickerSets`: Installed sticker packs.
- `actionOnStickerSet`: Add, remove, or reorder sticker packs.
- `addToMyGifSet`: Save GIF to favorites.

---

## 2. PWA & SuperApp Client Methods (`m.rubika.ir`) - 111 Methods

### 2.1 RUBINO (Social Network & Instagram Alternative - 65 Methods)
- **Feed & Explore:**
  - `getExplorePostTopics`: Topic categories for explore.
  - `getExplorePosts`: Infinite scroll explore media feed.
  - `getRelatedExplorePost`: Recommended posts based on current view.
  - `getRecentFollowingPosts`: Home timeline posts from followed creators.
  - `getPostsByHashTag`: Explore posts by hashtag.
  - `getHashTagTrend`: Trending hashtags on Rubino.
- **Posts & Interactions:**
  - `addPost` / `addFilePost` / `publishPost`: Create and publish image/video post.
  - `likePostAction`: Like / unlike post.
  - `getPostLikes`: List users who liked a post.
  - `postBookmarkAction` / `getBookmarkedPosts`: Save / unsave posts.
  - `addComment` / `addReplyComment`: Post comment or thread reply.
  - `getComments` / `getCommentReplies`: Load comments tree.
  - `likeCommentAction` / `getLikedCommentProfiles`: Comment likes.
- **Stories & Reels:**
  - `getProfilesStories` / `getStoryIds` / `getStory`: Stories feed and viewer.
  - `addViewStory`: Record story view impression.
  - `getStoryViewers`: List profiles who viewed story.
  - `deleteStory`: Remove published story.
  - `addPollAnswer` / `getPollResultsProfiles`: Interactive story polls.
  - `addEmojiSliderAnswer` / `getEmojiSliderResults`: Story emoji slider reactions.
  - `addHighlight` / `editHighlight` / `removeHighlightCollection`: Story highlights.
  - `getProfileHighlights` / `getHighlightStories`: Highlight collections.
  - `getLiveInfo` / `getLiveStatus` / `getLiveComments`: Rubino live streaming.
- **Profiles & Followers:**
  - `getProfileInfo` / `getMyProfileInfo`: Public and private profile stats.
  - `getProfilePosts` / `getMyProfilePosts`: Profile post grid.
  - `requestFollow` / `actionOnRequest`: Follow, unfollow, accept/reject requests.
  - `getProfileFollowers` / `searchFollower`: Follower/following lists.
  - `setBlockProfile` / `getBlockedProfiles`: Profile blocking.
  - `setReportRecord`: Report abusive profile/post.

### 2.2 NEW_VOD (Streaming Video on Demand - 18 Methods)
- `getMedia` / `getMediaByShareString`: Fetch media details and HLS playlist URLs.
- `getPlayInfo`: Retrieve playback tokens, video qualities, and DRM licenses.
- `getSeasonEpisodes`: List series seasons and episodes.
- `getRelated`: Related movies/series recommendations.
- `getCastDetails` / `getCastMedias`: Actor/Director filmographies.
- `getNextMediaInfo` / `getPlaySuggestedEpisode`: Next episode autoplay.
- `actionOnMedia`: Add to watchlist / like / dislike.
- `getWishList`: User saved watchlist.
- `search`: VOD catalog search.
- `setCurrentPlayTime` / `setSessionPlayDuration`: Sync watch progress.
- `getListing` / `getListItems` / `getCustomMenuItems`: VOD catalog categories.
- `viewCommercial`: Log ad view event.

### 2.3 WALLET (Rubika Digital Wallet & Payments - 6 Methods)
- `chargeWalletByToken`: Top-up balance using banking gateway token.
- `chargeWalletByUrl`: Generate banking payment URL.
- `checkAllowReceive`: Verify if recipient wallet can receive funds.
- `transferCredit`: Transfer funds between Rubika user wallets.
- `cashOut`: Withdraw funds to Iranian Sheba (IBAN) bank account.
- `getWalletByShareLink`: Resolve payment request link.

### 2.4 Discovery & Dynamic Services (`SERVICE` & `HOME` - 11 Methods)
- `getTiles`: Homepage discovery banner tiles.
- `getTagList` / `getTagObjects`: Dynamic category navigation.
- `getEndpointView` / `getEndpointData`: Service screen render descriptors.
- `searchQuery` / `getSearchStructure`: Universal search across mini-programs.
- `getExploreStructure` / `getDynamicPageData`: Dynamic JSON UI layouts.
- `setUserFavoriteServices`: Customize pinned shortcuts on the home screen.
- `getBarcodeAction`: Resolve Rubika QR code actions (payments, chats, channels).
- `getWebAppFunction`: Bridge API for Mini-Apps / Telegram WebApp equivalent.
