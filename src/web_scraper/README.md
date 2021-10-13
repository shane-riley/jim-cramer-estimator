# web_scraper

The web scraper (written in Python) will be a tool to grab stock articles from common websites.

The Scraper class leverages a json document 'tags.json' that provides custom methods for parsing field data for each site.

## Versions

- v1 (IN DEVELOPMENT): Grab an arbitrary number of pages from the test sites and write them to json files
- v2 (PLANNED): Grab an arbitrary number of pages from half of the full suite and write them to a local test DB
- v3 (PLANNED): Grab an arbitrary number of pages from the full suite and write them to a web database so the sentiment engine can run on a seperate machine

## Sites

Test Sites:

- [MarketWatch](https://www.marketwatch.com/)
- [Yahoo Finance](https://finance.yahoo.com/)

Full Suite:

- [MarketWatch](https://www.marketwatch.com/)
- [Yahoo Finance](https://finance.yahoo.com/)
- [Investing.com](https://www.investing.com/)
- [Wall Street Journal](https://www.wsj.com/)
- [Financial Times](https://www.ft.com/)
- [Seeking Alpha](https://seekingalpha.com/)
- [Zacks Investment Research](https://www.zacks.com/)
- [CNBC](https://www.cnbc.com/investing/)
- [InvestingNews](https://investingnews.com/)
- [Motley Fool](https://www.fool.com/investing-news/)
- [Barrons](https://www.barrons.com/)
- [USAToday](https://www.usatoday.com/money/investing/)
- [Wall Street Bets?](https://www.reddit.com/r/wallstreetbets/)