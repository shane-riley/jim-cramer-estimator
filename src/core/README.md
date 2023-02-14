# core

This folder contains class definitions and modules to be shared across components

## Article

Article objects represent parsed site articles with opinions on certain stocks at certain times

The Article class contains the following:

- tickers: list of relevant stocks
- author: Person that wrote the article
- date: Date of publication
- site: Site of origin
- url: URL of origin
- text: Body of the article

## API Driver
This class handles the API authentication and requests to provide historical stock data and other requests as needed.

### If refresh token is invalid...
1) Use this link: https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=http%3A%2F%2Flocalhost&client_id={ CLIENT_ID }%40AMER.OAUTHAP
2) Login with a valid Ameritrade account (not developer account)
3) Url decode everything in address bar after code=
4) Go to https://developer.tdameritrade.com/authentication/apis/post/token-0
5) Use the following parameters
	- grant_type authorization_code
	- access_type offline
	- code {URL_DECODED_CODE}
	- client_id {CLIENT_ID}
	- redirect_uri http://localhost
6) Paste the refresh_token into refresh_token.key
7) ApiDriver.py can now handle reauth again

## Data Driver
This class handles the local database storing the stock data.
In the future this should be moved to a larger storage server when the web app is running

## Sentiment

Sentiment objects represent opinions about tickers from certain Sources at a certain time

## Source

A Source is a combination of site and author, such that credibility can be determined for an individual author or an entire site.