from datetime import datetime
import json

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

    def json_dump(self, name: str) -> None:
        """
        Writes object into json file with given name

        Args:
            name (str): file location
        """

        jsonStr = json.dumps(self.__dict__, indent=4, sort_keys=True, default=str)

        with open(name, 'w') as f:
            f.write(jsonStr)