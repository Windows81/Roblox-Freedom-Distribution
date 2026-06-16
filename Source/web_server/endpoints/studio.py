# Standard library imports
import json
import time

# Local application imports
import util.versions as versions
from web_server._logic import web_server_handler, server_path


@server_path('/studio/e.png')
def _(self: web_server_handler) -> bool:
    self.send_data(b'')
    return True


@server_path('/login/RequestAuth.ashx')
def _(self: web_server_handler) -> bool:
    self.send_data(self.hostname + '/login/negotiate.ashx')
    return True


@server_path('/v2/login')
def _(self: web_server_handler) -> bool:
    try:
        # Password must not contain '1'.  This for debugging purposes only.
        assert (
            '1' not in json.loads(self.read_content())['password']
        )
        self.send_response(200)
        self.send_header('set-cookie', '.ROBLOSECURITY=_ROBLOSECURITY_')
        self.send_json({
            'user': {
                'id': 1630228,
                'name': 'qwer',
                'displayName': 'qwer',
            },
            'isBanned': False,
        }, status=None)
    except Exception:
        self.send_response(401)
    return True


@server_path('/Users/1630228')
@server_path('/game/GetCurrentUser.ashx')
def _(self: web_server_handler) -> bool:
    time.sleep(2)  # HACK: Studio 2021E won't work without it.
    self.send_json(1630228)
    return True


@server_path('/users/account-info')
def _(self: web_server_handler) -> bool:
    try:
        user_id_num = json.loads(self.headers['Roblox-Session-Id'])['UserId']
    except TypeError:
        return True

    funds = self.server.storage.funds.check(user_id_num) or 0
    self.send_json({
        "Roles": ["Soothsayer", "BetaTester"],
        "UserId": user_id_num,
        "RobuxBalance": funds,
    })
    return True


@server_path('/device/initialize')
def _(self: web_server_handler) -> bool:
    self.send_json({"browserTrackerId": 0, "appDeviceIdentifier": None})
    return True


@server_path('/v1/users/authenticated')
def _(self: web_server_handler) -> bool:
    self.send_json({
        "id": 1,
        "name": "ROBLOX",
        "displayName": "ROBLOX"
    })
    return True


@server_path('/my/settings/json', commands={'GET'})
def _(self: web_server_handler) -> bool:
    self.send_json({})
    return True


@server_path('/universal-app-configuration/v1/behaviors/studio/content')
def _(self: web_server_handler) -> bool:
    self.send_json(
        {
            "AssetManager": {
                "EnableAudioImport": True
            },
            "BetaFeaturesDialog": {
                "ShowDetailsButton": True
            },
            "BulkImporter": {
                "ShowCostInfo": False,
                "Enabled": True,
                "FreeAudioDevForumUrl": "https://devforum.roblox.com/t/action-needed-upcoming-changes-to-asset-privacy-for-audio/1701697"
            },
            "CaptchaDialog": {
                "AppNameSpecifier": ""
            },
            "ChallengeDialog": {
                "AppNameSpecifier": ""
            },
            "ChatWidget": {
                "HasEmptyDisabledText": False
            },
            "CloudEditModel": {
                "ChatEnabled": True
            },
            "ExternalLoginDialog": {
                "CookieDomain": "",
                "LoginUrl": ""
            },
            "GameSettings": {
                "AutoTranslationAllowed": False,
                "AutoTranslationTargetLanguages": {},
                "DisablePrivateServersAndPaidAccess": False,
                "OptInLocationsRequirements": {},
                "PlayerAppDownloadLink": {},
                "SocialMediaReferencesAllowed": True,
                "ShowBadges": True,
                "ShowOptInLocations": False
            },
            "LoginManager": {
                "ShowExternalLogin": False,
                "HideStartPageUrlLinks": False,
                "ShowPrivacyPolicyLinks": True,
                "ShowExternalLoginLink": False,
                "UserFacingWebsite": "",
                "WebView2SetupUrl": "https://create.roblox.com/docs/getting-started/setting-up-roblox-studio",
                "DistributorType": "Global"
            },
            "luaToolboxAction": {
                "Enabled": True
            },
            "MassUpdater": {
                "VersionConflictErrMsg": "Studio.App.StudioDataModelLoadUtil.ErrorCannotOpenTCPlaceDueToVersionConflictGlobal"
            },
            "PlaceVersionHistoryDialog": {
                "CanOpenHelpPage": True,
                "CreateFooterBar": True
            },
            "PlayerEmulator": {
                "SocialMediaReferencesAllowed": True
            },
            "PublishPlaceAs": {
                "OptInLocationsRequirements": {},
                "PlayerAppDownloadLink": {},
                "ShowOptInLocations": False
            },
            "StudioUserPreferences": {
                "PreferredLocale": "en_US"
            },
            "StudioUtilities": {
                "AppNameSpecifier": "",
                "PrivacyPolicyUrl": "https://en.help.roblox.com/hc/en-us/articles/115004630823-Roblox-Privacy-and-Cookie-Policy-",
                "TermsOfUseUrl": "https://en.help.roblox.com/hc/en-us/articles/115004647846-Roblox-Terms-of-Use",
                "ContactUsUrl": "https://www.roblox.com/support"
            },
            "Toolbox": {
                "DisableMarketplaceAndRecents": False,
                "ShowRobloxCreatedAssets": False,
                "MarketplaceDisabledCategories": "",
                "Enabled": True,
                "HomeViewEnabledAssetTypes": "Model",
                "MarketplaceShouldUsePluginCreatorWhitelist": False,
                "DisableRatings": False,
                "HideNonRelevanceSorts": True,
                "HideAssetConfigDistributeLearnMoreLink": False,
                "CreatorMarketplaceWebUrl": "https://create.roblox.com/store/",
                "VerificationDocumentationUrl": "https://create.roblox.com/docs/production/publishing/creator-marketplace#verifying-your-account",
                "AudioPrivacyLearnMoreUrl": "https://devforum.roblox.com/t/action-needed-upcoming-changes-to-asset-privacy-for-audio/1701697",
                "SafetyLearnMoreUrl": "https://en.help.roblox.com/hc/en-us/articles/203313410",
                "CreatorDashboardBaseUrl": "https://create.roblox.com/dashboard",
                "MarketplaceAssetConfigUrl": "https://create.roblox.com/dashboard/creations/store/%s/configure",
                "CreatorDashboardCatalogConfigUrlExtension": "/creations/catalog/%d/configure",
                "AnnouncementConfiguration": {
                    "ButtonKey": "Button_Default",
                    "Date": "2023-02-28 18:49:42",
                    "HeaderKey": "Header_02-28-2023",
                    "DescriptionKey": "Description_02-28-2023",
                    "Image": None,
                    "LinkLocation": None,
                    "LinkKey": "LinkText_Default",
                    "LatestUserId": "",
                    "IXPComparisonDefinitionKey": "QueryOptions",
                    "IXPComparisonVariableKey": "DomainSearchAlgorithmName"
                },
                "AssetConfigMessaging": {
                    "showManageUniversePermissionsLink": True,
                    "audioPublicationDisabledLink": "https://devforum.roblox.com/t/action-needed-upcoming-changes-to-asset-privacy-for-audio/1701697#can-i-change-the-privacy-settings-on-my-audio-assets-to-make-them-all-public-13"
                },
                "AssetConfigDistributionQuotas": {
                    "Model": {
                        "link": "https://create.roblox.com/docs/production/publishing/creator-store"
                    },
                    "Decal": {
                        "link": "https://create.roblox.com/docs/production/publishing/creator-store"
                    },
                    "Mesh": {
                        "link": "https://create.roblox.com/docs/production/publishing/creator-store"
                    },
                    "MeshPart": {
                        "link": "https://create.roblox.com/docs/production/publishing/creator-store"
                    },
                    "Plugin": {
                        "link": "https://create.roblox.com/docs/production/publishing/creator-store"
                    }
                },
                "AssetTypesWithAssetConfigFiatPrice": {
                    "Plugin": True,
                    "Model": False
                }
            },
            "UpdateArbiter": {
                "IsChinaBuild": False
            },
            "WebView": {
                "CaptchaHost": "static.rbxcdn.com",
                "ChallengeHost": "static.rbxcdn.com"
            },
            "WhatsNewWindow": {
                "Enabled": True,
                "DevForumRootUrl": "https://devforum.roblox.com/",
                "DevForumUrlSuffix": "tags/c/36/studio"
            }
        }
    )
    return True
