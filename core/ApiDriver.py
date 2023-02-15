import requests
import logging

from datetime import datetime, timedelta



class TDAPI():
	"""
	Wrapper for the TD Ameritrade API\n
	Handles ensuring requests are authenticated properly, automattically refreshes authentications when expired\n
	Provides wrapper methods for API calls to abstract it away from the rest of the program, only needing to 
	provide the arguments and receiving data as a return
	
	""" 

	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.retreive_client()
		self.retreive_refresh()
		self.retreive_auth()

	def retreive_client(self):
		"""
		Gets the client ID from the file, required to make any calls
		"""
		with open("auth_tokens/client_token.key", "r") as f:
			self.client_token = f.readline().strip()

	def retreive_refresh(self):
		"""
		Get the refresh token from the file system. Create a new one if invalid or about to expire
		"""
		with open("auth_tokens/refresh_token.key", "r") as f:
			self.refresh_tok = f.readline().strip()
			auth_time = f.readline()
			if auth_time == "":
				self.refresh_refresh()
				return
			auth_time = datetime.strptime(auth_time, "%m/%d/%Y, %H:%M:%S")
			if datetime.now() > auth_time + timedelta(days=80):
				self.refresh_refresh()

	def retreive_auth(self):
		"""
		Get the current auth token. Create a new one if invalid or expired
		"""
		with open("auth_tokens/auth_token.key", "r") as f:
			self.auth_tok = f.readline().strip()
			auth_time = f.readline()
			if auth_time == "":
				self.refresh_auth()
				return
			auth_time = datetime.strptime(auth_time, "%m/%d/%Y, %H:%M:%S")
			self.auth_time = auth_time
			if datetime.now() > auth_time + timedelta(minutes=30):
				self.refresh_auth()
	
	def check_auth(func):

		def wrapper(self, *args, **kwargs):
			if datetime.now() > self.auth_time + timedelta(minutes=30):
				self.refresh_auth()
			return func(self, *args, **kwargs)
		
		return wrapper

	def refresh_auth(self):
		"""
		Create a new auth token. Should be used every 30 minutes
		"""
		resp = requests.post("https://api.tdameritrade.com/v1/oauth2/token", data={"grant_type": "refresh_token", "refresh_token": self.refresh_tok, "client_id" : self.client_token}).json()
		if "error" in resp:
			self.logger.debug(resp)
			self.logger.critical("UNABLE TO CREATE NEW AUTH TOKEN")
			return 
		with open("auth_tokens/auth_token.key", "w") as f:
			f.write(resp["access_token"]+"\n")
			f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
			self.auth_tok = resp["access_token"]
			self.auth_time = datetime.now()

	def refresh_refresh(self):
		"""
		Create a new refresh token. Should be used every ~80 days
		"""
		resp = requests.post("https://api.tdameritrade.com/v1/oauth2/token", data={"grant_type": "refresh_token", "refresh_token": self.refresh_tok, "access_type": "offline", "client_id" : self.client_token, "redirect_uri" : ""}).json()
		self.logger.debug(resp)
		with open("auth_tokens/refresh_token.key", "w") as f:
			f.write(resp["refresh_token"]+"\n")
			f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
			self.refresh_tok = resp["refresh_token"]

	@check_auth	
	def get_history(self, ticker="", periodType="day", period="10", frequencyType="minute", frequency="1", start_epoch=0, end_epoch=0, datetime_str=False):
		"""
		Get the historical data from a stock. If using epochs for time period no need to specify period argument

		ticker -- The ticker of the stock to get the history of\n
		periodType -- {day, month, year, ytd} the unit for period\n
		period -- {"day" : [1, 2, 3, 4, 5, 10], "month" : [1,2,3,6], "year" : [1, 2, 3, 5, 10, 15, 20], "ytd" : 1} how much history to return for the ticker\n
		frequencyType -- {"day" : "minute", "month" : ["daily","weekly"], "year" : ["daily", "weekly", "monthly"], "ytd" : ["daily", "weekly"]} frequency that a new chunk is created\n
		frequency -- {"minute" : ["1", "5", "10", "15", "30"], "daily" : "1", "weekly" : "1", "monthly" : "1"} number of frequencyType in each chunk\n
		start_epoch -- POSIX timestamp in seconds to begin. Must be int not float
		end_epoch -- POSIX timestamp in seconds to end. Must be int not float
		datetime_str -- Convert date to a human readable time. Not to be used for database records
		"""
		self.logger.debug(f"Querying API for {ticker}")
		headers = {"Authorization" : f"Bearer {self.auth_tok}"}
		
		if start_epoch == 0:
			resp = requests.get(f"https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory", params={"periodType" : periodType, "period" : period, "frequencyType" : frequencyType, "frequency": frequency}, headers=headers).json()
		else:
			resp = requests.get(f"https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory", params={"periodType" : periodType, "frequencyType" : frequencyType, "frequency": frequency, "endDate" : end_epoch*1000, "startDate" : start_epoch*1000}, headers=headers).json()

		if "error" in resp:
			self.logger.critical(f"CANNOT COMPLETE REQUEST ----- {resp}")
			return "ERROR" + resp["error"]
		
		for x in resp["candles"]:
			x["datetime"] = x["datetime"]/1000
			if datetime_str:
				x["datetime"] = datetime.fromtimestamp(x["datetime"]).strftime("%m/%d/%Y, %H:%M:%S")

		self.logger.debug(f"API RETURNED {resp}")
		return resp["candles"]
		
