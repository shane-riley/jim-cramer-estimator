from datetime import datetime

class Logger:
	"""
	Class to handle different levels of logging to different output locations
	"""
	def __init__(self, level=1, out=0, path=None):
		"""
		level: Only output logs with at least this level.
				Logs can have 5 levels:
				1- DEBUG
				2- INFO
				3- WARNING
				4- ERROR
				5- CRITICAL
		out: 0, 1, or 2
				Use 0 to print to stdout, use 1 to create a default logging file, use 2 to use a custom path
		path: Only to be used if out=2, the path to save the logging file to, without a trailing '/'
		"""
		if not 0 < level <= 6:
			raise ValueError("Logging level is in an invalid range!")
		if not 0 <= out <=2:
			raise ValueError("Output is in an invalid range!")
		
		self.level = level
			
		if out == 1:
			self.file = open(f'Logs/LOG_{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log', 'w')
		if out == 2:
			self.file = open(f'{path}/LOG_{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log', 'w')
		self.out = out

	def __log(self, s, level):
		if level >= self.level:
			if self.out == 0:
				print(s)
			else:
				self.file.write(s)
				self.file.write("\n")
	
	def debug(self, s):
		s = f"Debug: {str(s)}"
		self.__log(s, 1)

	def info(self, s):
		s = f"Info: {str(s)}"
		self.__log(s, 2)

	def warn(self, s):
		s = f"WARNING: {str(s)}"
		self.__log(s, 3)

	def error(self, s):
		s = f"---ERROR: {str(s)}"
		self.__log(s, 4)

	def critical(self, s):
		s = f"\n-----CRITICAL: {str(s)}\n"
		self.__log(s, 5)

	def close(self):
		self.file.close()