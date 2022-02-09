from src.core.ApiDriver import TDAPI
from src.core.DataDriver import DataDriver
from datetime import datetime
from src.logging.Logger import Logger
from src.web_scraper.USNewsScraper import USNewsScraper
from src.web_scraper.YFScraper import YFScraper

log = Logger(level=1, out=2, path="Logs/Tests")

usscrape = USNewsScraper(logger=log)
yfscrape = YFScraper(logger=log)

tester = TDAPI(logger=log)
start = datetime.strptime("10/9/2019", "%m/%d/%Y")
end = datetime.strptime("12/9/2019", "%m/%d/%Y")
ret = tester.get_history(ticker="GSPC", periodType="year", frequencyType="weekly", start_epoch=int(datetime.timestamp(start)*1000), end_epoch=int(datetime.timestamp(end)*1000))
log.info(str(ret))

data = DataDriver(logger=log)
data.calculate_historical("TSLA", start=1612210000000, end=1632210000000)

art = usscrape.parse_article("https://money.usnews.com/investing/stock-market-news/articles/ipo-stocks-to-watch-this-month")
log.info(art.json_dump())

yahoo_art = yfscrape.parse_article("https://finance.yahoo.com/news/a-meta-morphosis-in-market-sentiment-morning-brief-100754611.html")
log.info(yahoo_art.json_dump())

data.insert_article(art.json_dump())
data.insert_article(yahoo_art.json_dump())

log.close()
