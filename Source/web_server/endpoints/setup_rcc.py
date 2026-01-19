from web_server._logic import web_server_handler, server_path
import util.versions as versions
import re


@server_path('/api.GetAllowedMD5Hashes/')
def _(self: web_server_handler) -> bool:
    '''
    TODO: apply and test patches to completely skip over this endpoint.
    '''
    self.send_json({
        "data": [
            "696224eb7537fbd4f684d05b30e7577b",
            "852c653bf5524615b0c16d08c7888489",
            "4f2255d00b498e8728394d44033375f1",
            "3228e65cf0a1a5efb11c1f50bc7e0e72",
            "2e3625c467dce071ef0366eb01f360b2",
            "d32f2f383eb067dbf4cef929e3720d22",
            "4f2255d00b498e8728394d44033375f1",
            "c51ce865a76f65834e0f9ed837ed1014",
            "f82d895f557e45d8ca779bd02729e8e5",
            "57b38d86235db049d8fbea3ac9ad0368",
            "a228078a3575428fb9bec8b158a563ca",
            "382edacdb1ea130cae005cda632490ca",
            "21560a2399a218dcfe56c7603bd37e20",
            "b41a1f6db3d35705d76ffad110add0b6",
            "7ffd87ec48186fd302d70762958792b6",
            "34394c67cf26408c24c4c68e447b465e",
            "da6e066c4db1df5561eb5a5eee06615a",
            "0395956deb4a80d4532e5cd8e24640e0",
            "cddb32998e61bb8a88d71b235bceb546",
            "034dad52f899219be7f974184908e7bb",
            "ba2258bbb24cd7ac772f8bc4bcc0c347",
            "12c35dfa6e96cf0cdbe45d2632806f54",
            "f1a5abf74dfc2c882ab95ca7c7d89129",
            "25cb4fa68e2b70a484a6cb7255a4a9d3",
            "08832dcb9f771b3436021de228017148",
            "641c9bee9332eea0bd91aae83ad206c9",
            "adc4983c75ab1b5b990f3bd30bf03949",
            "33fbddac973e93485c7e7d884d271724",
            "972dd1995553445d3bd9c7e4b8e08b26",
            "bff0c728dd9eb6224311be4628474791",
            "0904ee91b51adb48ae6d066606b469c2",
            "20a13e1db27108fb7fd1375366f1c0b5",
            "471c84516a9eead73c13d5369dc3fa51",
            "3231d09a8c3525a75e999789aa7d9df4",
        ]
    })
    return True


@server_path(r'/v[12]/autolocalization/games/(\d+)/autolocalizationtable', regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({
        "isAutolocalizationEnabled": False,
        "shouldUseLocalizationTable": False,
    })
    return True


@server_path('/api.GetAllowedSecurityVersions/', versions={versions.rōblox.v347})
def _(self: web_server_handler) -> bool:
    self.send_json({
        'data': [
            '0.348.0pcplayer',
            '2.348.0androidapp',
        ],
    })
    return True


@server_path('/api.GetAllowedSecurityVersions/', versions={versions.rōblox.v463})
def _(self: web_server_handler) -> bool:
    self.send_json({
        'data': [
            '0.463.0pcplayer',
            '2.463.0androidapp',
        ],
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
