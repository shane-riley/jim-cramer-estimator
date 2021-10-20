"""
Sample Yahoo Finance Article Scraper (run in main directory)
"""

from src.web_scraper.YFScraper import YFScraper
import os

TEST_AUTHOR = 'Javier E David'
TEST_OUT_FOLDER = 'test_out'

try:
    os.mkdir(TEST_OUT_FOLDER)
except Exception:
    pass

yf = YFScraper()

# Use the author page to get a list of article urls
urls = yf.get_urls_from_author(TEST_AUTHOR)

# Parse articles and write to json
for i in range(len(urls)):
    url = urls[i]
    try:
        json_name = os.path.join(TEST_OUT_FOLDER, TEST_AUTHOR.replace(' ', '-') + '_' + str(i).zfill(3) + '.json')
        art = yf.parse_article(url)
        art.json_dump(json_name)
        print(f'PARSED: {url}')
    except Exception:
        print(f'FAILED: {url}')






