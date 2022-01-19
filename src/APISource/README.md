## If refresh token is invalid...
1) Use this link: https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=http%3A%2F%2Flocalhost&client_id={ CLIENT_ID }%40AMER.OAUTHAP
2) Login with a valid Ameritrade account (not developer account)
3) Url decode everything in address bar after code=
4) Go to https://developer.tdameritrade.com/authentication/apis/post/token-0
5) Use the following parameters
	- grant_type authorization_code
	- access_type offline
	- code {URL_DECODED_CODE}
	- redirect_uri http://localhost
6) Paste the refresh_token into refresh_token.key
7) ApiDriver.py can now handle reauth again