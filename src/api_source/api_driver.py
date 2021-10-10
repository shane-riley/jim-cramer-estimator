import requests
from datetime import datetime, timedelta


class TDAPI():

	def __init__(self):
		self.retreive_client()
		self.retreive_refresh()
		self.retreive_auth()

	def retreive_client(self):
		"""
		Gets the client ID from the file, required to make any calls
		"""
		with open("client_token.key", "r") as f:
			self.client_token = f.readline().strip()

	def retreive_refresh(self):
		"""
		Get the refresh token from the file system. Create a new one if invalid or about to expire
		"""
		with open("refresh_token.key", "r") as f:
			self.refresh_tok = f.readline().strip()
			auth_time = f.readline()
			if auth_time == "":
				self.refresh_refresh()
			auth_time = datetime.strptime(auth_time, "%m/%d/%Y, %H:%M:%S")
			if datetime.now() > auth_time + timedelta(days=80):
				self.refresh_refresh()

	def retreive_auth(self):
		"""
		Get the current auth token. Create a new one if invalid or expired
		"""
		with open("auth_token.key", "r") as f:
			self.auth_tok = f.readline().strip()
			auth_time = f.readline()
			if auth_time == "":
				self.refresh_auth()
				return
			auth_time = datetime.strptime(auth_time, "%m/%d/%Y, %H:%M:%S")
			if datetime.now() > auth_time + timedelta(minutes=30):
				self.refresh_auth()
	
	def refresh_auth(self):
		"""
		Create a new auth token. Should be used every 30 minutes
		"""
		resp = requests.post("https://api.tdameritrade.com/v1/oauth2/token", data={"grant_type": "refresh_token", "refresh_token": self.refresh_tok, "client_id" : self.client_token}).json()
		if "error" in resp:
			print(resp)
			print("UNABLE TO CREATE NEW AUTH TOKEN")
			return 
		with open("auth_token.key", "w") as f:
			f.write(resp["access_token"]+"\n")
			f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

	def refresh_refresh(self):
		"""
		Create a new refresh token. Should be used every ~80 days
		"""
		resp = requests.post("https://api.tdameritrade.com/v1/oauth2/token", data={"grant_type": "refresh_token", "refresh_token": self.refresh_tok, "access_type": "offline", "client_id" : self.client_token, "redirect_uri" : ""}).json()
		print(resp)
		with open("refresh_token.key", "w") as f:
			f.write(resp["refresh_token"]+"\n")
			f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
		
	def get_history(self, ticker, periodType="day", period="2", frequencyType="minute", frequency="1"):
		"""
		ticker -- The ticker of the stock to get the history of\n
		periodType -- {day, month, year, ytd} the unit for period\n
		period -- {"day" : [1, 2, 3, 4, 5, 10], "month" : [1,2,3,6], "year" : [1, 2, 3, 5, 10, 15, 20], "ytd" : 1} how much history to return for the ticker\n
		frequencyType -- {"day" : "minute", "month" : ["daily","weekly"], "year" : ["daily", "weekly", "monthly"], "ytd" : ["daily", "weekly"]} frequency that a new chunk is created\n
		frequency -- {"minute" : ["1", "5", "10", "15", "30"], "daily" : "1", "weekly" : "1", "monthly" : "1"} number of frequencyType in each chunk\n

		"""
		headers = {"Authorization" : f"Bearer {self.auth_tok}"}
		resp = requests.get(f"https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory", data={"periodType" : periodType, "period" : period, "frequencyType" : frequencyType, "frequency": frequency}, headers=headers).json()["candles"]
		for x in resp:
			print(datetime.fromtimestamp(x["datetime"]/1000))
		
