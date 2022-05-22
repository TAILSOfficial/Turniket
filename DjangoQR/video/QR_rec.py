# from cryptography.fernet import Fernet
from django.conf import settings
from datetime import datetime
from loguru import logger

from .models import data as _db_data
from .models import enter

import RPi.GPIO as GPIO
import threading
import atexit
import time
import cv2
import sys
import os


def numerator() -> int:
	i = 0
	while True:
		yield i
		i += 1
num = numerator()
for i in os.listdir('imgs'):
	next(num)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
atexit.register(GPIO.cleanup)

def save_img(group: str, fio: str, date: datetime) -> None:
	nuf = f'{str(next(num))}.jpg'
	path = os.path.join(os.path.join(os.getcwd(), 'imgs'), nuf)
	enter(group = group, name = fio, path_to_img = path, date = datetime.now()).save()
	fr = getattr(sys, 'VideoPortal')[1].frame.copy()
	cv2.imwrite(path, fr)

def go_away():
	GPIO.output(23, GPIO.HIGH)
	time.sleep(5)
	GPIO.output(23, GPIO.LOW)


def start():
	detector = cv2.QRCodeDetector()
	hash_prev_data = None
	prev_time = 0

	import sys

	while not getattr(sys, 'VIDCAP_EXIT_FLAG'):
		time.sleep(0.1)
		if not getattr(sys, 'VideoPortal')[0].used_frame:
			img = getattr(sys, 'VideoPortal')[0].frame
		else:
			continue

		try:
			data, bbox, _ = detector.detectAndDecode(img)
		except Exception as e:
			logger.exception(e)
		
		if (bbox is not None):
			for i in range(len(bbox)):
				a = tuple([int(k) for k in bbox[i][0]])
				b = tuple([int(k) for k in bbox[(i+1) % len(bbox)][1]])

			if data:
				try:
					cv2.line(img, a, b, color = (255, 0, 0), thickness = 2)
					# data = cipher.decrypt(data.encode('utf-8')).decode('utf-8')
					fio, group = data.split(', ')
					lst = _db_data.users_dict()
					if fio in lst.keys() and (hash(data) != hash_prev_data or time.time() - prev_time >= 7):
						if group == lst[fio]:
							threading.Thread(target = go_away).start()
							cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
										1, (0, 255, 0), 2)
							threading.Thread(target = save_img, args = (group, fio, datetime.now())).start()
							hash_prev_data = hash(data)
							prev_time = time.time()
						else:
							cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
										1, (255, 0, 0), 2)
					else:
						cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
									1, (255, 0, 0), 2)
						
				except Exception as e:
					logger.exception(e)

		if 'CV_WINDOW' in os.environ.keys():
			cv2.imshow("code detector", img)


@atexit.register
def if_exit():
	cv2.destroyAllWindows()