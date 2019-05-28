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
list_for_litter = {'*departure_all*': 'Departures.pdf', '*arrchkinbyroom*': 'Arrival and checked in today.pdf', '*gibyroom*': 'Guest in house (by room).pdf', '*finopbalall*': 'Open balance (individuals).pdf'}

tm = datetime.datetime.now()
os.chdir(src)
files = os.listdir(src)

logging.basicConfig(filename='//172.27.1.8/d$/offline_reports/info.log', level=logging.INFO)
logging.info('Дата исполнения: %s' % tm)
# поиск файла Departures
files_departure = [file for file in fnmatch.filter(files, '*departure_all*')]
if files_departure:
    files_departure = max(files_departure, key=os.path.getctime)
    logging.info('Последний файл Departures: %s' % files_departure)
else:
    logging.info('Последний файл Departures не найден')

# поиск файла arrival and checked in today
files_arrchkinbyroom = [file for file in fnmatch.filter(files, '*arrchkinbyroom*')]
if files_arrchkinbyroom:
    files_arrchkinbyroom = max(files_arrchkinbyroom, key=os.path.getctime)
    logging.info('Последний файл arrival and checked in today: %s' % files_arrchkinbyroom)
else:
    logging.info('Последний файл arrival and checked in today не найден')

# поиск файла Guest in house (by room)
files_gibyroom = [file for file in fnmatch.filter(files, '*gibyroom*')]
if files_gibyroom:
    files_gibyroom = max(files_gibyroom, key=os.path.getctime)
    logging.info('Последний файл Guest in house (by room): %s' % files_gibyroom)
else:
    logging.info('Последний файл Guest in house (by room) не найден')

# поиск файла Open balance (individuals)
files_finopbalall = [file for file in fnmatch.filter(files, '*finopbalall*')]
if files_gibyroom:
    files_finopbalall = max(files_finopbalall, key=os.path.getctime)
    logging.info('Последний файл Open balance (individuals): %s' % files_finopbalall)
else:
    logging.info('Последний файл Open balance (individuals) не найден')

files_del = [files_departure, files_arrchkinbyroom, files_finopbalall, files_gibyroom]

for dst in list_for_pc:
    if os.path.isfile(files_departure):
        shutil.copy2(files_departure, dst + 'Departures.pdf', follow_symlinks=True)
        logging.info('Файл %s скопирован в %s' % (files_departure, dst))
    else:
        logging.info('Файл не найден')
    if os.path.isfile(files_arrchkinbyroom):
        shutil.copy2(files_arrchkinbyroom, dst + 'Arrival and checked in today.pdf', follow_symlinks=True)
        logging.info('Файл %s скопирован в %s' % (files_arrchkinbyroom, dst))
    else:
        logging.info('Файл не найден')
    if os.path.isfile(files_gibyroom):
        shutil.copy2(files_gibyroom, dst + 'Guest in house (by room).pdf', follow_symlinks=True)
        logging.info('Файл %s скопирован в %s' % (files_gibyroom, dst))
    else:
        logging.info('Файл не найден')
    if os.path.isfile(files_finopbalall):
        shutil.copy2(files_finopbalall, dst + 'Open balance (individuals).pdf', follow_symlinks=True)
        logging.info('Файл %s скопирован в %s' % (files_finopbalall, dst))
    else:
        logging.info('Файл не найден')

logging.info('************Удаление файлов на сервере***********')
for file in files_del:
    if os.path.isfile(file):
        os.remove(file)
        logging.info('Файл %s удален успешно' % file)
    else:
        logging.info('Файл %s ненайден' % file)
