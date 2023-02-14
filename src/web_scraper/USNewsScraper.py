import re
import logging

from requests import HTTPError, get
from bs4 import BeautifulSoup
from datetime import datetime

from src.web_scraper.BaseScraper import BaseScraper
from src.core.Article import Article

"""
TODO: How to scrape the slideshow articles?

""" 

class USNewsScraper(BaseScraper):

	SITE_NAME = 'US News'
	def __init__(self, logger=None):
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
		art.title = soup.find('h1', {'class': re.compile("Heading__HeadingStyled.*")}).text

		# Tickers

		#Check if using iframe ticker display
		ticker_elems = soup.find_all('div', {'class': 'tradingview-widget-copyright'}) 
		if ticker_elems:
			ticker_getter = re.compile("/symbols/.*/")
			for elem in ticker_elems:
				ticker = ticker_getter.search(elem.contents[0]["href"]).group(0)[9:-1] 
				logging.debug(ticker)
				art.tickers.add(ticker)
		else:
			#If no iframe, get from the article headers
			ticker_elems = soup.find_all('h3', {'class': 'heading-large'})
			ticker_getter = re.compile("\(\w*\)")
			for elem in ticker_elems:
				ticker = ticker_getter.search(elem.text)
				if ticker:
					ticker = ticker.group(0)[1:-1]
					logging.debug(ticker)
					art.tickers.add(ticker)
			
		# Author
		art.author = soup.find('a', {'class': re.compile(".*BylineArticle__AuthorAnchor.*")}).text

		# Date
		art.date = soup.find('span', {'class': re.compile(".*byline-article-date-span")}).text
		art.date = int(datetime.strptime(art.date, "%b. %d, %Y").timestamp()*1000)

		# Site
		art.site = self.SITE_NAME
	
		# URL
		art.url = url

		# Text
		art.text = soup.find('div', {'id': "ad-in-text-target"}).text
		
		return art






