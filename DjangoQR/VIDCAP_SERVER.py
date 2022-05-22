from datetime import datetime
from loguru import logger
from typing import Any

import Db_connector
import threading
import socket
import pickle
import struct
import numpy
import time
import cv2
import os


ip = '127.0.0.1'
ports = 5672, 5673

detector = cv2.QRCodeDetector()

class SocketServer:
	def __init__(self, ip: str, port: int):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((ip, port))
		self.server.listen(5)
		self.clients = {}

		threading.Thread(target = self.sock_accept).start()

	def sock_accept(self) -> None:
		while True:
			conn, addr = self.server.accept()
			self.clients.update({conn: addr})

	def mailing(self, source: Any) -> None:
		while True:
			a = pickle.dumps(source)
			message = struct.pack("Q", len(a)) + a
			for client in self.clients.keys():
				client.send(message)


class VideoCamera:
	def __init__(self, cam_id: int):
		self.server = SocketServer(ip, ports[cam_id])

		try:
			self.video = cv2.VideoCapture(cam_id)
			self.grabbed, self.frame = self.video.read()
			threading.Thread(target = self.update, args = ()).start()
		except:
			self.frame = numpy.zeros((640, 480, 3))

		if cam_id == 1:
			threading.Thread(target = self.server.mailing, args = (self.frame,))

	def __del__(self):
		self.video.release()

	def update(self):
		while True:
			self.grabbed, self.frame = self.video.read()
			time.sleep(0.1)


cam0 = VideoCamera(0)
cam1 = VideoCamera(1)

def numerator() -> int:
    i = 0
    while True:
        yield i
        i += 1
num = numerator()
for i in os.listdir('imgs'):
    next(num)

def save_img(group: str, fio: str, date: datetime) -> None:
	global cam1

	nuf = f'image_{str(next(num))}.jpg'
	path = os.path.join(os.path.join(os.getcwd(), 'imgs'), nuf)
	Db_connector.log_in_db(group, fio, path, datetime.now())

	fr = cam1.frame.copy()
	cv2.imwrite(path, fr)

while True:
	img = cam0.frame.copy()

	try:
		data, bbox, _ = detector.detectAndDecode(cam0.frame)
	except Exception as e:
		logger.exception(e)
	
	if (bbox is not None):
		for i in range(len(bbox)):
			a = tuple([int(k) for k in bbox[i][0]])
			b = tuple([int(k) for k in bbox[(i + 1) % len(bbox)][1]])

		if data:
			try:
				cv2.line(img, a, b, color = (255, 0, 0), thickness = 2)
				fio, group = data.split(', ')
				lst = Db_connector.get_members_dict()
				if fio in lst.keys() and hash(data) != hash_prev_data:
					if group == lst[fio]:
						cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
									1, (0, 255, 0), 2)
						threading.Thread(target = save_img, args = (group, fio, datetime.now())).start()
						hash_prev_data = hash(data)
					else:
						cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
									1, (255, 0, 0), 2)
				else:
					cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
								1, (255, 0, 0), 2)

				a = pickle.dumps(frame)
				message = struct.pack("Q", len(a)) + a
				for client in cam0.server.clients.keys():
					client.send(message)
					
			except Exception as e:
				logger.exception(e)

	cv2.imshow('Cam0', img)

cap.release()
cv2.destroyAllWindows()