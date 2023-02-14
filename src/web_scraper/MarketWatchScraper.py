import logging
import re

from requests import HTTPError
from bs4 import BeautifulSoup
from datetime import datetime

from src.web_scraper.BaseScraper import BaseScraper
from src.core.Article import Article

"""
TODO: How to scrape t he slideshow articles?

"""

class MarketWatchScraper(BaseScraper):

	SITE_NAME = 'Market Watch'
	def __init__(self):
		pass

	def get_url(self, index: int) -> str:
		"""
		Leverage a robots.txt file or a sitemap\n
		to get URL's corresponding to articles
		
		Args:
			index (int): Article index to ensure uniqueness.\n
			0 represents the most recent article URL
		
		Returns:
			str: story URL

		"""
		raise NotImplementedError

	def parse_article(self, url: str) -> Article:
		"""
		Parse a URL article into an Article object

		Args:
			url (str): Location of webpage

		Returns:
			Article: Parsed Article
		
		Throws:
			RuntimeError: If article fields fail to be populated

		"""
		
		# Attempt to download article
		try:
			html_doc = super().download_article(url)
		except HTTPError:
			# Failed to download, reraise
			raise Exception

		# Article downloaded, parse
		art = Article()
		soup = BeautifulSoup(html_doc, 'html.parser')

		# Title
		art.title = soup.find('h1', {'class': 'article__headline'}).text

		# Tickers
		tickers = soup.findAll('span', {'class': 'symbol'})
		for ticker in tickers:
			art.tickers.add(ticker.text)
		
		
			
		# Author
		art.author = soup.find('h4', {'itemprop': 'name'}).text

		# Date
		update = 0

		art.date = soup.find('time', {'class': 'timestamp timestamp--update'}).text
		if not art.date:
			update = 1
			art.date = soup.find('time', {'class': 'timestamp timestamp--pub'}).text
		
		art.date = re.sub('\s+', ' ', art.date)[1:-4]
		logging.debug(art.date[-4:])
		if art.date[-4:] == "a.m.":
			art.date = art.date[:-4] + "AM"
		if art.date[-4:] == "p.m.":
			art.date = art.date[:-4] + "PM"
		
		if update == 0:
			art.date = int(datetime.strptime(art.date, "Last Updated: %b. %d, %Y at %I:%M %p").timestamp()*1000)
		else:
			art.date = int(datetime.strptime(art.date, "Published: %b. %d, %Y at %I:%M %p").timestamp()*1000)

		# Site
		art.site = self.SITE_NAME
	
		# URL
		art.url = url

		# Text
		# TODO: change this to only scrape <p> from this div
		art.text = soup.find('div', {'id': 'js-article__body'}).text
		
		return art






