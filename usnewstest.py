from src.web_scraper.USNewsScraper import USNewsScraper
from src.logging.Logger import Logger

log = Logger(level=1, out=2, path="Logs/scraping_test")
scrape = USNewsScraper(logger=log)

art = scrape.parse_article("https://money.usnews.com/investing/stock-market-news/articles/ipo-stocks-to-watch-this-month")
log.info(art.json_dump())