import os

pc061 = '//172.27.2.61/c$/Offline_opera_reports/'
if os.access(pc061, os.W_OK):
    print('ok')
else:
    print('NO')

