from src.core.ApiDriver import TDAPI
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.logging.Logger import Logger

class DataDriver():
	def __init__(self, logger=None):
		if not logger:
			self.log = Logger(level=3, out=1)
		else:
			self.log = logger	
		self.API = TDAPI(self.log)


	def connect_stock(self):
		self.stock_db = sqlite3.connect("stocks.db")
		self.stock_db_cur = self.stock_db.cursor()
		try:
			self.stock_db_cur.execute("SELECT * FROM stocks LIMIT 1")
		except sqlite3.OperationalError:
			self.stock_db_cur.execute("CREATE TABLE stocks (ticker text, date real, price real)")

	def connect_articles(self):
		self.art_db = sqlite3.connect("articles.db")
		self.art_db_cur = self.art_db.cursor()
		




	def calculate_historical(self, ticker, start, end=datetime.timestamp(datetime.now())*1000):
		"""
		Pull data from cache, or request new from api and store in database

		start: Must be in milliseconds. Note datetime.timestamp returns in seconds
		"""
		result = self.stock_db_cur.execute(f"SELECT * FROM stocks WHERE ticker='{ticker}' AND date >= {start} AND date <= {end}")
		row = result.fetchall()
		if row:
			self.log.debug(f"Pulled from database: {row}")
		else:
			self.log.debug("Not in database, calling API")
			self.fetch_historical(ticker, start, end)


	def fetch_historical(self, ticker, start, end):
		data = self.API.get_history(ticker=ticker, periodType="year", frequencyType="weekly", start_epoch=int(start), end_epoch=int(end), datetime_str=False)
		for row in data:
			self.stock_db_cur.execute(f"INSERT INTO stocks VALUES ('{ticker}', {row['datetime']}, {row['close']})")
		self.stock_db.commit()




