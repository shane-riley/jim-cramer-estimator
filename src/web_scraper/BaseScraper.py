from abc import ABC, abstractmethod
from src.core.Article import Article

import requests

class BaseScraper(ABC):
	"""
	An abstract base class that defines methods for finding urls\n
	and scraping URL's for Article objects
	"""

	@abstractmethod
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
		pass

	@abstractmethod
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
		pass
	
	def download_article(self, url: str) -> str:
		"""
		Download an article and return the HTML body

		Args:
			url (str): Location of webpage

		Returns:
			str: HTML body

		Throws:
			HTTPError: If article fields fail to be populated
			
		"""

		h = {'User-Agent': 'Custom'}
		r = requests.get(url, headers=h)
		r.raise_for_status()
		return r.text





