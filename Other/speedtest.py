"""
    Before using, you must install speedtest-cli python library.
    Just run the following command pip install speedtest-cli.
"""

print('Program in processing, please wait')

import re
import subprocess
import time

print('Assembly of informations\n')
response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode()

ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

ping = ping[0].replace(',', '.')
download = download[0].replace(',', '.')
upload = upload[0].replace(',', '.')

print('Preparing of report\n')
print('Report:\ndate {}, time {},\nping {}, '
      'download {}, upload {}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, download, upload))

input()
