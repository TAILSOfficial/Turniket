from loguru import logger
from rich import print
from time import sleep

import sys
import os


p = os.popen('python manage.py runserver', 'r')

for line in iter(p.readline, b''):
	sleep(0.01)
	if line.rstrip() == "":
		continue
	line = line.rstrip().replace('[', '{').replace(']', '}')
	try:
		print(line)
	except KeyboardInterrupt:
		p.close()
		exit()
	except Exception as e:
		print(line)
		logger.exception(e)