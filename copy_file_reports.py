import os
import shutil
import fnmatch
import logging
import datetime

src = '//172.27.1.8/d$/Micros/opera/export/OPERA/altay'
pc061 = '//172.27.2.61/c$/Offline_opera_reports/'
pc062 = '//172.27.2.62/c$/Offline_opera_reports/'
pc063 = '//172.27.2.63/c$/Offline_opera_reports/'
pc066 = '//172.27.2.66/c$/Offline_opera_reports/'
pc065 = '//172.27.2.65/c$/Offline_opera_reports/'
list_for_pc = [pc061, pc062, pc063, pc065, pc066]
list_for_litter = {'*departure_all*': 'Departures.pdf', '*arrchkinbyroom*': 'Arrival and checked in today.pdf',
                   '*gibyroom*': 'Guest in house (by room).pdf', '*finopbalall*': 'Open balance (individuals).pdf'}

tm = datetime.datetime.now()
os.chdir(src)
files = os.listdir(src)

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', filename='//172.27.1.8/d$/offline_reports/info.log', level=logging.INFO)
logging.info('Дата исполнения: %s\n' % tm)

for filter_file in list_for_litter.keys():
    search_file = [file for file in fnmatch.filter(files, filter_file)]
    if search_file:
        search_file = max(search_file, key=os.path.getctime)
        logging.info('Последний файл %s: %s\n' % (list_for_litter.get(filter_file), search_file))
        if os.path.isfile(search_file):
            for dst in list_for_pc:
                if os.access(dst, os.W_OK):
                    shutil.copy2(search_file, dst + list_for_litter.get(filter_file), follow_symlinks=True)
                    logging.info('Файл %s скопирован в %s\n' % (search_file, dst))
                else:
                    logging.info('Удаленый каталог %s не доступен' % dst)
            os.remove(search_file)
            logging.info('Файл %s удален успешно\n' % search_file)
        else:
            logging.info('Не является файлом\n')
    else:
        logging.info('Последний файл %s не найден\n' % list_for_litter.get(filter_file))
