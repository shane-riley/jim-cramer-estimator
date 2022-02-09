from src.web_scraper.BaseScraper import BaseScraper
from src.core.Article import Article
from src.logging import Logger

from requests import HTTPError
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import isoparse

class YFScraper(BaseScraper):
    """
    Web Scraper for Yahoo Finance
    """
    def __init__(self, logger=None):
        if not logger:
            self.log = Logger(level=3, out=1)
        else:
            self.log = logger


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

    def get_urls_from_author(self, author: str) -> list:
        """
        Get a sample list of stories corresponding to an author
        
        Args:
            author (str): Author name
        
        Returns:
            list: list of story URL's

        """

        # Make the link
        author = author.replace(' ', '-').lower()
        url = f'https://www.yahoo.com/author/{author}'

        # Download the article
        soup = BeautifulSoup(super().download_article(url), 'html.parser')

        # Look at the availible links
        urls = []
        for link in soup.find_all('a'):
            url = link['href']
            if "https://finance.yahoo.com/news" in url:
                urls.append(url)

        # NOTE: The YF Author pages have buttons that reveal more links. Accessing older links is more complex than a page download
        
        return urls



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
        art.date = int(isoparse(soup.find('time')['datetime']).timestamp() * 1000)

        # Site
        art.site = self.SITE_NAME
    
        # URL
        art.url = url

        # Text
        art.text = soup.find('div', {'class': 'caas-body'}).text
        
        return art

        
