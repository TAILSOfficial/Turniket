from django.http import StreamingHttpResponse, Http404, HttpResponse
from django.shortcuts import render
from django.conf import settings

import sys


# Create your views here.
def gen(college_name: str):
	while True:
		try:
			frame = sys.Colleges_frames[college_name]
		except KeyError:
			frame = None
		if frame is not None:
			yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
		else:
			break


def view(request, college_name: str = None) -> StreamingHttpResponse | HttpResponse:
	if not college_name:
		return render(request, 'video_responses.html', {'colleges': settings.get_env('colleges')})
	else:
		if college_name not in sys.Colleges_frames.keys():
			raise Http404('College Not Found')
		else:
			return StreamingHttpResponse(gen(college_name), content_type = "multipart/x-mixed-replace;boundary=frame")
