from web_server._logic import web_server_handler, server_path
import util.versions as versions
import util.const


@server_path('/api.GetAllowedMD5Hashes/')
def _(self: web_server_handler) -> bool:
    self.send_json(util.const.ALLOWED_MD5_HASHES)
    return True


@server_path('/api.GetAllowedSecurityVersions/')
def _(self: web_server_handler) -> bool:
    self.send_json({
        'data': self.game_config.game_setup.roblox_version.security_versions(),
    })
    return True


@server_path('/game/load-place-info')
@server_path('/.127.0.0.1/game/load-place-info')
@server_path('/.127.0.0.1/game/load-place-info/')
def _(self: web_server_handler) -> bool:
    self.send_json({
        'CreatorId': 0,
        'CreatorType': 'User',
        'PlaceVersion': 1,
        'GameId': 123456,
        'IsRobloxPlace': True,
    })
    return True


@server_path('/v1.1/Counters/BatchIncrement')
@server_path('/v1.0/SequenceStatistics/BatchAddToSequencesV2')
def _(self: web_server_handler) -> bool:
    self.send_json({})
    return True


@server_path('/universal-app-configuration/v1/behaviors/app-patch/content')
def _(self: web_server_handler) -> bool:
    self.send_json({
        "SchemaVersion": "1",
        "CanaryUserIds": [],
        "CanaryPercentage": 0
    })
    return True


@server_path('/universal-app-configuration/v1/behaviors/app-policy/content')
def _(self: web_server_handler) -> bool:
    self.send_json({
        "ChatConversationHeaderGroupDetails": True,
        "ChatHeaderSearch": True,
        "ChatHeaderCreateChatGroup": True,
        "ChatHeaderHomeButton": False,
        "ChatHeaderNotifications": True,
        "ChatPlayTogether": True,
        "ChatShareGameToChatFromChat": True,
        "ChatTapConversationThumbnail": True,
        "ChatViewProfileOption": True,
        "GamesDropDownList": True,
        "UseNewDropDown": False,
        "GameDetailsMorePage": True,
        "GameDetailsShowGlobalCounters": True,
        "GameDetailsPlayWithFriends": True,
        "GameDetailsSubtitle": True,
        "GameInfoList": True,
        "GameInfoListDeveloper": True,
        "GamePlaysAndRatings": True,
        "GameInfoShowBadges": True,
        "GameInfoShowCreated": True,
        "GameInfoShowGamepasses": True,
        "GameInfoShowGenre": True,
        "GameInfoShowMaxPlayers": True,
        "GameInfoShowServers": True,
        "GameInfoShowUpdated": True,
        "GameReportingDisabled": False,
        "GamePlayerCounts": True,
        "GiftCardsEnabled": False,
        "Notifications": True,
        "OfficialStoreEnabled": False,
        "RecommendedGames": True,
        "SearchBar": True,
        "MorePageType": "More",
        "AboutPageType": "About",
        "FriendFinder": True,
        "SocialLinks": True,
        "SocialGroupLinks": True,
        "EnableShareCaptureCTA": True,
        "SiteMessageBanner": True,
        "UseWidthBasedFormFactorRule": False,
        "UseHomePageWithAvatarAndPanel": False,
        "UseBottomBar": True,
        "AvatarHeaderIcon": "LuaApp/icons/ic-back",
        "AvatarEditorShowBuyRobuxOnTopBar": True,
        "HomeIcon": "LuaApp/icons/ic-roblox-close",
        "ShowYouTubeAgeAlert": False,
        "GameDetailsShareButton": True,
        "CatalogShareButton": True,
        "AccountProviderName": "",
        "InviteFromAccountProvider": False,
        "ShareToAccountProvider": False,
        "ShareToAccountProviderTimeout": 8,
        "ShowDisplayName": True,
        "GamesPageCreationCenterTitle": False,
        "ShowShareTargetGameCreator": True,
        "SearchAutoComplete": True,
        "CatalogShow3dView": True,
        "CatalogReportingDisabled": False,
        "CatalogCommunityCreations": True,
        "CatalogPremiumCategory": True,
        "CatalogPremiumContent": True,
        "ItemDetailsFullView": True,
        "UseAvatarExperienceLandingPage": True,
        "HomePageFriendSection": True,
        "HomePageProfileLink": True,
        "PurchasePromptIncludingWarning": False,
        "ShowVideoThumbnails": True,
        "VideoSharingTestContent": [],
        "SystemBarPlacement": "Bottom",
        "EnableInGameHomeIcon": False,
        "UseExternalBrowserForDisclaimerLinks": False,
        "ShowExitFullscreenToast": True,
        "ExitFullscreenToastEnabled": False,
        "UseLuobuAuthentication": False,
        "CheckUserAgreementsUpdatedOnLogin": True,
        "AddUserAgreementIdsToSignupRequest": True,
        "UseOmniRecommendation": True,
        "ShowAgeVerificationOverlayEnabled": False,
        "ShouldShowGroupsTile": True,
        "ShowVoiceUpsell": False,
        "ProfileShareEnabled": True,
        "ContactImporterEnabled": True,
        "FriendCodeQrCodeScannerEnabled": False,
        "RealNamesInDisplayNamesEnabled": False,
        "CsatSurveyRestrictTextInput": False,
        "RobloxCreatedItemsCreatedByLuobu": False,
        "GameInfoShowChatFeatures": True,
        "PlatformGroup": "Unknown",
        "UsePhoneSearchDiscoverEntry": False,
        "HomeLocalFeedItems": {
            "UserInfo": 1,
            "FriendCarousel": 2
        },
        "Routes": {
            "auth": {
                "connect": "v2/login",
                "login": "v2/login",
                "signup": "v2/signup"
            }
        },
        "PromotionalEmailsCheckboxEnabled": True,
        "PromotionalEmailsOptInByDefault": False,
        "EnablePremiumUserFeatures": True,
        "CanShowUnifiedChatUpsell": True,
        "RequireExplicitVoiceConsent": True,
        "RequireExplicitAvatarVideoConsent": True,
        "EnableVoiceReportAbuseMenu": True
    })
    return True
