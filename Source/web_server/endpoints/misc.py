import time
import json

from web_server._logic import web_server_handler, server_path


@server_path(r'/Setting/Get/AndroidAppSettings/')
def _(self: web_server_handler) -> bool:
    '''
    https://github.com/conewasnthere/unix-src/blob/58ef6b9b6cb59921552a9d4bb2de8783db579736/Setting/Get/AndroidAppSettings/index.php
    '''
    self.send_json({
        "GoogleVideoAdUrl": "",
        "AdColonyZoneId": "",
        "AdColonyAppId": "",
        "EnableRbxAnalytics": "False",
        "UseNewWebGamesPage": "False",
        "GigyaPrefix": "",
        "EnabledSponsoredZoom": "False",
        "EnableUtilsAlertFix": "True",
        "EnableFacebookAuth": "False",
        "EnableGameStartFix": "False",
        "EnableGoogleAnalyticsChange": "False",
        "FIntAvatarEditorAndroidRollout": "1",
        "FIntEnableAvatarEditorAndroid": "1",
        "FIntEnableAvatarEditoriOS": "100",
        "EnableCookieConsistencyChecks": "False",
        "EnableRotationGestureFix": "True",
        "EnableRbxReportingManager": "False",
        "EnableInfluxV2": "False",
        "InfluxUrl": "",
        "InfluxDatabase": "",
        "InfluxUser": "",
        "InfluxPassword": "",
        "InfluxThrottleRate": "0",
        "EnableNeonBlocker": "True",
        "EnableLoginFailureExactReason": "True",
        "EnableLoginWriteOnSuccessOnly": "False",
        "EnableXBOXSignupRules": "False",
        "EnableInputListenerActivePointerNullFix": "False",
        "EnableWelcomeAnimation": "False",
        "EnableShellLogoutOnWebViewLogout": "False",
        "EnableSetWebViewBlankOnLogout": "False",
        "EnableLoginLogoutSignupWithApi": "False",
        "EnableSessionLogin": "True",
        "AndroidInferredCrashReporting": "False",
        "EnableAuthCookieAnalytics": "False"
    })
    return True


@server_path(r'/v1.1/Counters/Increment/')
def _(self: web_server_handler) -> bool:
    '''
    https://github.com/astralsc/scythe/blob/3cbfaaec99c8e3db9996288534c5c29da0036758/src/public/v1.1/Counters/Increment/index.php#L5
    '''
    self.send_json({
        "success": True,
        "counterName": self.query.get("counterName", ""),
        "amount": self.query.get("amount", 0),
        "timestamp": '2026-05-26 13:50:55',
        "postDataReceived": False,
    })
    return True


# MOCK DATABASE
# Replace this dictionary with your actual DB connector later.
# Structure mirrors the SQL: SELECT * FROM `users` WHERE `name`= :username
MOCK_DB = {
    '67': {
        'id': 1630228,
        'token': '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhwKBGR1aWQSFDEzNjcwOTI5Mzc2NTU2MTY1NDcyKAM.tgDCk1jAKYAzEUR9d3h2ckQPulAIFNO7HYpIprVIlCp6zqRg36SbQxV7HeJe_GgjbOsGdxCRVmDvEYfXUZ-d7yv_Dy4pdhgfvxIvMWoG6XVbmMTNbsx2kt2eJCwHyZo7F1QLSt2mJUqvo_QKb5IDma7qJQdsq9nrUGhP7ee4IyjAlXFcUzs3j9SChdsoOLNJOBXl46LgyUG4fymeMpVgc0EujmNH6jScZgI8YGWeilcOrKpjzzqQq_u2JMxCW9lRh2q7mdtTtNq3i9PtFYvCh9RImwe35rzS7vu28lRUnYWhYfVd6i9mRnWat5_q3vUYYOiBgW2pQmJvSZpLHWejOKTvvAVUJggugJsA-RJvbz0bPNw-3EsOC1FlTFd73HTwZdw_npUc3rDn6uqHBMLskVUKjtjyce5XbWcJMIjE1GRTQdIK5f6qaNbLcysXZDgR-rI9p1hf2hxPJ74A1mTYB6583wwL83CNU_nO4nBUzOUsGlVEVQrhCe1W6NaL3lwsYDcg3G_PHIRqc6KsRxLVLppMxRH7VvuIPnZBUZraofZ0VqKKtL-jBfRHFbuQbkWWEKOTN3De_5wgzwH00WCx9jZdSGct9eIJSw7VmLZxKQnOXbE2Z7oSyT-pCCrnUk4_wtjMDPo7aIfXkqlsC-fzmp96_-aYjIQ5sXPfe0ALpiCRx_mreuQpjaY6DvRt-N8EPE_3r_9xRP8__6KCBfRTolvlLZG05nLGa98xprd5R228v6STUo6qKQJ_5FQzC9i10SHY_oXOzu8UTRg50FDEDd-nh-A',
        'password': '67'  # Plain text for mock simplicity
    }
}

# The code below was written by Qwen3.6-35B-A3B.


@server_path('/v2/login')
def _(self: web_server_handler) -> bool:
    try:
        # 1. Parse input (JSON body or form-urlencoded)
        raw_content = self.read_content()
        # Safe header access depending on your framework's API
        user_agent = getattr(self, 'headers', {}).get('User-Agent', '')

        username = password = None
        data = json.loads(raw_content)
        username = data.get('username', data.get('cvalue', None))
        password = data.get('password', None)

        # PHP's strip_tags equivalent

        if not username or not password:
            self.send_json(
                {'message': 'Username and password are required.'}, status=400)
            return True

        # 2. Mock Database Query
        user_data = MOCK_DB.get(username)

        if not user_data:
            self.send_json({'message': 'Incorrect username.'}, status=403)
            return True

        # 3. Password Verification
        # Using plain string comparison since this is a mock database.
        if user_data.get('password') != password:
            self.send_json(
                {'message': 'Incorrect password. Please try again.'}, status=403)
            return True

        # 4. Extract user data
        roblosec = user_data['token']
        uid = user_data['id']
        display_name = username

        # 5. Set Cookies
        # PHP uses: time() + (460800 * 30) seconds
        expiry_time = time.time() + (460800 * 30)

        # 6. Return JSON
        self.send_json({
            'membershipType': 4,
            'username': display_name,
            'isUnder13': False,
            'countryCode': "US",
            'userId': uid,
            'displayName': display_name
        }, headers={
            'Set-Cookie': f'.ROBLOSECURITY={roblosec}',
        })

    except Exception:
        self.send_response(401)
    return True


@server_path('/Users/1630228')
@server_path('/game/GetCurrentUser.ashx')
def _(self: web_server_handler) -> bool:
    time.sleep(2)  # HACK: Studio 2021E probably won't work without it.
    self.send_json(1630228)
    return True


@server_path('/users/account-info')
def _(self: web_server_handler) -> bool:
    self.send_json({
        "UserId": 1630228,
        "Username": '67',
        "DisplayName": '67',
        "HasPasswordSet": True,
        "Email": {"Value": 'n**@roblox.com', "IsVerified": True},
        "AgeBracket": 0,
        "Roles": ['BetaTester', 'Beta17', 'Roblox.Slack.Models.Contractor.Name', 'Soothsayer'],
        "MembershipType": 0,
        "RobuxBalance": 98763,
        "NotificationCount": 223,
        "EmailNotificationEnabled": False,
        "PasswordNotificationEnabled": False,
        "CountryCode": 'RU',
    })
    return True


@server_path('/incoming-items/counts')
def _(self: web_server_handler) -> bool:
    self.send_json({
        "unreadMessages": 0,
        "unansweredFriendRequests": 0,
    })
    return True


@server_path('/mobileapi/check-app-version')
def _(self: web_server_handler) -> bool:
    self.send_json({"data": {"UpgradeAction": "None"}})
    return True


@server_path('/ab/v1/enroll')
def _(self: web_server_handler) -> bool:
    self.send_json({"baller": "baller"})
    return True


@server_path('/home')
def _(self: web_server_handler) -> bool:
    self.send_data("<body>UwU</body>")
    return True
