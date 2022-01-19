from src.APISource.ApiDriver import TDAPI
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.logging.Logger import Logger

class DataDriver():
	def __init__(self, logger=None):
		self.database = sqlite3.connect("stocks.db")
		self.database_cur = self.database.cursor()
		self.API = TDAPI()
		try:
			self.database_cur.execute("SELECT * FROM stocks LIMIT 1")
		except sqlite3.OperationalError:
			self.database_cur.execute("CREATE TABLE stocks (ticker text, date real, price real)")
		if not logger:
			self.log = Logger(level=3, out=1)
		else:
			self.log = logger		

	def calculate_historical(self, ticker, start, end=""):
		"""
		Pull data from cache, or request new from api and store in database
		"""
		result = self.database_cur.execute(f"SELECT * FROM stocks WHERE ticker='{ticker}'")
		row = result.fetchall()
		if row:
			self.log.debug(row)
		else:
			self.fetch_historical(ticker, start, end)


	def fetch_historical(self, ticker, start, end):
		data = self.API.get_history(ticker=ticker, periodType="year", frequencyType="weekly", start_epoch=int((datetime.now() - relativedelta(months=6)).timestamp()), end_epoch=int(datetime.now().timestamp()), datetime_str=False)
		for row in data:
			self.database_cur.execute(f"INSERT INTO stocks VALUES ('{ticker}', {row['datetime']}, {row['close']})")
		self.database.commit()




