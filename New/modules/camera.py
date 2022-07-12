from threading import Thread

import numpy
import cv2


class Camera:
	def __init__(self, camera_id: int):
		self.node = cv2.VideoCapture(camera_id)
		self.frame = numpy.zeros((480, 640, 3))
		Thread(target = self.update).start()

	def update(self):
		_ = True
		while _:
			_, self.frame = self.node.read()
		self.frame = numpy.zeros((480, 640, 3))