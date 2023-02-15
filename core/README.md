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
This class handles the raw SQL interactions.

### Postgres local setup
1) Install postgres, ensure \bin is on path
2) Ensure postgres server is running 
	-D is the directory where postgres will store the databases
	pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start
3) Execute command 'createdb stocks'
4) Ensure there is a user which can login and make changes to the database
	Use postgres user for local testing
	4a) To create a user, use psql stocks, CREATE USER xxx SUPERUSER PASSWORD 'xxx'
		Use other roles than superuser if needed, may have to grant specific permissions to tables in the db for the user if not a superuser
5) Change login information in DataDriver connect_db() for psycopg2.connect() 

## Sentiment

Sentiment objects represent opinions about tickers from certain Sources at a certain time

## Source

A Source is a combination of site and author, such that credibility can be determined for an individual author or an entire site.