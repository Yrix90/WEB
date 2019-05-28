import logging
import datetime

logging.basicConfig(filename='//172.27.1.8/d$/offline_reports/info.log', level=logging.INFO)

a = 3
b = 6
c = a + b
tm = datetime.datetime.now()
logging.info('test %s' % tm)
