from datetime import datetime
import logging
import os

from core.DataDriver import DataDriver

from web_scraper.MarketWatchScraper import MarketWatchScraper
from web_scraper.USNewsScraper import USNewsScraper
from web_scraper.YFScraper import YFScraper

def init_logger():
	try:
		os.mkdir(f"Logs/")
	except Exception:
		pass
	logging.basicConfig(filename=f'Logs/{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log', filemode='w', level=logging.DEBUG)

def main():
	init_logger()
	logger = logging.getLogger(__name__)

	usscrape = USNewsScraper()
	yfscrape = YFScraper()
	MWScrape = MarketWatchScraper()
	data = DataDriver()


	with open("web_scraper/mw.txt", 'r') as f:
		for line in f:
			art = MWScrape.parse_article(line)
			data.insert_article(art.json_dump())

	with open("web_scraper/usnews.txt", 'r') as f:
		for line in f:
			art = usscrape.parse_article(line)
			data.insert_article(art.json_dump())
    
	with open("web_scraper/yf.txt", 'r') as f:
		for line in f:
			art = yfscrape.parse_article(line)
			data.insert_article(art.json_dump())


if __name__ == "__main__":
	main()