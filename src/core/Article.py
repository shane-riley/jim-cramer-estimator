from datetime import datetime
import json

class Article():
    """
    Data class for containing article information\n
    Comes from the scraper, goes to the sentiment engine\n
    Stored in the database as article table rows
    """

    def __init__(self):
            # Instance variables
        self.tickers = set()
        self.author  = ""
        self.date    = None
        self.site    = ""
        self.url     = ""
        self.text    = ""
        self.title   = ""

    def json_dump(self, name=None) -> str:
        """
        Writes object into json file with given name, or if no name given return as a string

        Args:
            name (str): file location, or none to return a string
        """

        jsonStr = json.dumps(self.__dict__, indent=4, sort_keys=True, default=str)
        if name:
            with open(name, 'w') as f:
                f.write(jsonStr)
            return "OUTPUT TO FILE!"
        return jsonStr