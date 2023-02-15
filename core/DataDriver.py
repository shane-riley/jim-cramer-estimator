import psycopg2
import logging

from datetime import datetime

from core.ApiDriver import TDAPI


class DataDriver():
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.API = TDAPI()
		self.connect_db()

	def connect_db(self):
		self.db = psycopg2.connect(host="localhost", dbname="stocks", user="manager") 
		db_cur = self.db.cursor()
		db_cur.execute("select exists(select * from information_schema.tables where table_name='stocks')")
		if not db_cur.fetchone()[0]:
			db_cur.execute("CREATE TABLE stocks (ticker text, date real, price real)")
			db_cur.execute(f"CREATE TABLE articles (article_id SERIAL PRIMARY KEY, site text)")
			db_cur.execute(f"CREATE TABLE tickers (ticker_id SERIAL PRIMARY KEY, ticker text, article_id integer, FOREIGN KEY(article_id) REFERENCES articles(article_id))")
			db_cur.close()
			self.db.commit()
		else:
			self.logger.debug("Tables already created, skipping")

	def insert_article(self, json):
		"""
		The article JSON is expected to have the following keys:\n
		author, date, site, text, tickers, title, url\n
		date should be a UNIX timestamp in seconds\n

		If these keys are not present, data will be missing from the database entry
		"""
		with self.db.cursor() as db_cur:
			db_cur.execute(f"select exists(select * from information_schema.tables where table_name='{json['site']}')")
			if not db_cur.fetchone()[0]:
				db_cur.execute(f"CREATE TABLE {json['site']} (article_id integer, author text, date real, title text, content text, url text)")
			else:
				self.logger.debug(f"{json['site']} table already exists, skipping")
			
		with self.db.cursor() as db_cur:
			db_cur.execute(f"INSERT into articles (site) VALUES ('{json['site']}') RETURNING article_id")
			id = db_cur.fetchone()[0]
			db_cur.execute(f"INSERT into {json['site']}(article_id, author, date, title, content, url) VALUES ({id}, '{json['author']}', {json['date']}, '{json['title']}', '{json['text']}', '{json['url']}')")
			for ticker in json['tickers']:
				db_cur.execute(f"INSERT into tickers (ticker, article_id) VALUES ('{ticker}', {id})")

		with self.db.cursor() as db_cur:
			db_cur.execute("SELECT * FROM market_watch")
			self.logger.debug(db_cur.fetchall())

		self.db.commit()
	
	def fetch_article(self, site, author="", date=0, ticker=[], url=""):
		"""
		Dynamic method for retireving articles out of the database
		Arguments:
		(string) site: The name of the site the article(s) is(are) from 
		(string) author: The name of the author of the article(s). 
		(int) date: a UNIX timestamp in seconds corresponding to the date of the article(s).
		(list of string) ticker: A list containing the tickers to query from
		"""



	def calculate_historical(self, ticker, start, end=datetime.timestamp(datetime.now())):
		"""
		Pull data from cache, or request new from api and store in database

		start: Must be in seconds. Note datetime.timestamp returns in seconds
		"""
		db_cur = self.db.cursor()
		db_cur.execute(f"SELECT * FROM stocks WHERE ticker='{ticker}' AND date >= {start} AND date <= {end}")
		row = db_cur.fetchall()
		if row:
			self.logger.debug(f"Pulled from database: {row}")
		else:
			self.logger.debug("Not in database, calling API")
			self.fetch_historical(ticker, start, end)
		db_cur.close()


	def fetch_historical(self, ticker, start, end):
		data = self.API.get_history(ticker=ticker, periodType="year", frequencyType="weekly", start_epoch=int(start), end_epoch=int(end), datetime_str=False)
		db_cur = self.db.cursor()
		for row in data:
			db_cur.execute(f"INSERT INTO stocks VALUES ('{ticker}', {row['datetime']}, {row['close']})")
		db_cur.close()
		self.db.commit()




