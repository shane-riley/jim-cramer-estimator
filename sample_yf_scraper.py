"""
Sample Yahoo Finance Article Scraper (run in main directory)
"""

import json
from src.web_scraper.YFScraper import YFScraper
from src.logging.Logger import Logger
import os

TEST_AUTHOR = 'Brian Sozzi'
TEST_OUT_FOLDER = 'test_out'
log = Logger(2, out=2, path="Logs/scraping_test")

try:
    os.mkdir(TEST_OUT_FOLDER)
except Exception:
    pass

yf = YFScraper(log)

# Use the author page to get a list of article urls
urls = yf.get_urls_from_author(TEST_AUTHOR)

# Parse articles and write to json
for i in range(len(urls)):
    url = urls[i]
    try:
        json_name = os.path.join(TEST_OUT_FOLDER, TEST_AUTHOR.replace(' ', '-') + '_' + str(i).zfill(3) + '.json')
        art = yf.parse_article(url)
        json_string = art.json_dump()
        log.info(f'PARSED: {url}')
        log.info(json_name)
        log.info(json_string)
    except Exception:
        log.error(f'FAILED: {url}')






