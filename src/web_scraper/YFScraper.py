from src.web_scraper.BaseScraper import BaseScraper
from src.core.Article import Article

from requests import HTTPError
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import isoparse

class YFScraper(BaseScraper):
    """
    Web Scraper for Yahoo Finance
    """

    SITE_NAME = 'Yahoo Finance'

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
            Exception: If article fields fail to be populated

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
        art.title = soup.find_all('h1', {'data-test-locator': 'headline'})[0].text

        # Tickers
        ticker_elems = soup.find_all('div', {'data-entity-type': 'ticker'})
        for elem in ticker_elems:
            art.tickers.add(str(elem['data-entity-id']))


        # Author
        art.author = soup.find('span', {'class': 'caas-author-byline-collapse'}).text

        # Date
        art.date = isoparse(soup.find('time')['datetime'])

        # Site
        art.site = self.SITE_NAME
    
        # URL
        art.url = url

        # Text
        art.text = soup.find('div', {'class': 'caas-body'}).text
        
        return art

        
