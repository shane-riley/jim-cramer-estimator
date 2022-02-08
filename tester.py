from distutils.log import Log
from src.core.ApiDriver import TDAPI
from src.core.DataDriver import DataDriver
from datetime import datetime
from src.logging.Logger import Logger

log = Logger(level=1, out=2, path="Logs/API_test")

tester = TDAPI(logger=log)
start = datetime.strptime("10/9/2019", "%m/%d/%Y")
end = datetime.strptime("12/9/2019", "%m/%d/%Y")
ret = tester.get_history(ticker="MSFT", periodType="year", frequencyType="weekly", start_epoch=int(datetime.timestamp(start)*1000), end_epoch=int(datetime.timestamp(end)*1000))
log.info(str(ret))

data = DataDriver(logger=log)
data.calculate_historical("TSLA", start=1612210000000, end=1632210000000)

log.close()
