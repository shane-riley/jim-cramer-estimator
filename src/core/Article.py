from datetime import date
from typing import Set

class Article():
    """
    Data class for containing article information\n
    Comes from the scraper, goes to the sentiment engine\n
    Stored in the database as article table rows
    """

    # Instance variables
    tickers = set()
    author  = ""
    date    = None
    site    = ""
    url     = ""
    text    = ""
    title   = ""

    def __init__(self):
        # Do nothing
        pass