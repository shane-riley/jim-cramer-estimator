from distutils.log import Log
from src.APISource.ApiDriver import TDAPI
from src.credibility.DataDriver import DataDriver
from datetime import datetime
from src.logging.Logger import Logger

log = Logger(1, out=2, path="Logs/API_test")

tester = TDAPI(logger=log)
start = datetime.strptime("10/9/2019", "%m/%d/%Y")
end = datetime.strptime("12/9/2019", "%m/%d/%Y")
ret = tester.get_history(ticker="MSFT", periodType="year", frequencyType="weekly", start_epoch=int(datetime.timestamp(start)), end_epoch=int(datetime.timestamp(end)))
log.info('-----------')
log.info(str(ret))

data = DataDriver(logger=log)
data.calculate_historical("MSFT", start=datetime.now())

log.close()
