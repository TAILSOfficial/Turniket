from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.conf import settings
from loguru import logger

from . import QR_rec

import threading
import atexit
import numpy
import cv2
import sys


# Create your views here.
class VideoCamera(object):
	def __init__(self, cam_id: int):
		try:
			self.video = cv2.VideoCapture(cam_id)
			self.success = True
			_, self.frame = self.video.read()
			if self.frame is None:
				self.frame = numpy.zeros((480, 640, 3))
				self.success = False
			self.used_frame = False
		except Exception as e:
			# logger.exception(e)
			self.success = False
			self.frame = numpy.zeros((480, 640, 3))
		if self.success:
			self.thread = threading.Thread(target=self.update, args=())
			self.thread.start()

	def __del__(self) -> None:
		self.video.release()
		del self.video

	def get_frame(self) -> bytes:
		image = self.frame
		ret, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()

	def update(self) -> None:
		import time
		import sys

		while not getattr(sys, 'VIDCAP_EXIT_FLAG'):
			_, self.frame = self.video.read()
			if self.frame is None:
				break
			self.used_frame = False
			time.sleep(0.1)

		self.frame = numpy.zeros((480, 640, 3))


@atexit.register
def if_exit():
	try:
		for x in getattr(sys, 'VideoPortal'):
			try:
				setattr(sys, 'VIDCAP_EXIT_FLAG', True)
				x.thread.join()
			except:
				pass
	except:
		pass

@atexit.register
def if_exit2():
	try:
		setattr(sys, 'VIDCAP_EXIT_FLAG', True)
		getattr(sys, 'QR_REC_THREAD').join()
	except:
		pass


def get_VidCap(cam_id: int) -> VideoCamera:
	try:
		if not hasattr(sys, 'VideoPortal'):
			setattr(sys, 'VIDCAP_EXIT_FLAG', False)
			atexit.register(lambda: setattr(sys, 'VIDCAP_EXIT_FLAG', True))
			# atexit.register(lambda: [i for i in map(lambda x: x.thread._stop(), getattr(sys, 'VideoPortal'))])
			sys.VideoPortal = (VideoCamera(0), VideoCamera(1))

			qr_thread = threading.Thread(target = QR_rec.start, args = ())
			qr_thread.start()
			setattr(sys, 'QR_REC_THREAD', qr_thread)
			# atexit.register(lambda: getattr(sys, 'QR_REC_THREAD')._stop())

			if sys.VideoPortal[cam_id].success:
				return sys.VideoPortal[cam_id]

		else:
			if sys.VideoPortal[cam_id].success:
				return sys.VideoPortal[cam_id]
	except Exception as e:
		logger.exception(e)

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield(b'--frame\r\n'
			  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		if not camera.success:
			break


def cam0(request):
	cam = get_VidCap(0)
	if cam is not None:
		return StreamingHttpResponse(gen(cam), content_type = "multipart/x-mixed-replace;boundary=frame")
	else:
		return render(request, 'Cam_not_image.html')

def cam1(request):
	cam = get_VidCap(1)
	if cam is not None:
		return StreamingHttpResponse(gen(cam), content_type = "multipart/x-mixed-replace;boundary=frame")
	else:
		return render(request, 'Cam_not_image.html')