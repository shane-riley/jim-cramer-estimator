import sqlite3
import logging

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from src.core.ApiDriver import TDAPI

class DataDriver():
	def __init__(self):
		self.API = TDAPI()
		self.connect_stock()
		self.connect_articles()

	def connect_stock(self):
		self.stock_db = sqlite3.connect("stocks.db")
		self.stock_db_cur = self.stock_db.cursor()
		try:
			self.stock_db_cur.execute("SELECT * FROM stocks LIMIT 1")
		except sqlite3.OperationalError:
			self.stock_db_cur.execute("CREATE TABLE stocks (ticker text, date real, price real)")

		self.stock_db.commit()

	def connect_articles(self):
		"""
		Database structure: tickers <- article -> sites 
		"""
		self.art_db = sqlite3.connect("articles.db")
		self.art_db_cur = self.art_db.cursor()
		try:
			self.art_db_cur.execute(f"SELECT * FROM tickers LIMIT 1")
		except sqlite3.OperationalError:
			self.art_db_cur.execute(f"CREATE TABLE article (article_id integer PRIMARY KEY, site text)")
			self.art_db_cur.execute(f"CREATE TABLE tickers (ticker_id integer PRIMARY KEY, ticker text, article_id integer, FOREIGN KEY(article_id) REFERENCES articles(article_id))")
	
		self.art_db.commit()

	def insert_article(self, json):
		"""
		The article JSON is expected to have the following keys:\n
		author, date, site, text, tickers, title, url\n
		date should be a UNIX timestamp in milliseconds!\n

		If these keys are not present, data will be missing from the database entry
		"""
		try:
			self.art_db_cur.execute(f"SELECT * FROM '{json['site']}' LIMIT 1")
		except sqlite3.OperationalError:
			logging.debug("creating site table")
			self.art_db_cur.execute(f"CREATE TABLE '{json['site']}' (article_id integer, author text, date real, title text, content text, url text)")
			
		self.art_db_cur.execute(f"INSERT into article (site) VALUES ('{json['site']}')")
		id = self.art_db_cur.execute("SELECT last_insert_rowid()").fetchone()[0]
		self.art_db_cur.execute(f"INSERT into '{json['site']}'(article_id, author, date, title, content, url) VALUES ({id}, '{json['author']}', {json['date']}, '{json['title']}', '{json['text']}', '{json['url']}')")
		for ticker in json['tickers']:
			self.art_db_cur.execute(f"INSERT into tickers (ticker, article_id) VALUES ('{ticker}', {id})")
		
		self.art_db.commit()
	
	def fetch_article(self, site, author="", date=0, ticker=[], url=""):
		"""
		Dynamic method for retireving articles out of the database
		Arguments:
		(string) site: The name of the site the article(s) is(are) from 
		(string) author: The name of the author of the article(s). 
		(int) date: a UNIX timestamp in milliseconds corresponding to the date of the article(s).
		(list of string) ticker: A list containing the tickers to query from
		"""



	def calculate_historical(self, ticker, start, end=datetime.timestamp(datetime.now())*1000):
		"""
		Pull data from cache, or request new from api and store in database

		start: Must be in milliseconds. Note datetime.timestamp returns in seconds
		"""
		result = self.stock_db_cur.execute(f"SELECT * FROM stocks WHERE ticker='{ticker}' AND date >= {start} AND date <= {end}")
		row = result.fetchall()
		if row:
			logging.debug(f"Pulled from database: {row}")
		else:
			logging.debug("Not in database, calling API")
			self.fetch_historical(ticker, start, end)


	def fetch_historical(self, ticker, start, end):
		data = self.API.get_history(ticker=ticker, periodType="year", frequencyType="weekly", start_epoch=int(start), end_epoch=int(end), datetime_str=False)
		for row in data:
			self.stock_db_cur.execute(f"INSERT INTO stocks VALUES ('{ticker}', {row['datetime']}, {row['close']})")
		self.stock_db.commit()




