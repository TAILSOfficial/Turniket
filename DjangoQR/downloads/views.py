from django.http import FileResponse, Http404
from django.shortcuts import render
from django.conf import settings


# Create your views here.
def index(request, file_name: str) -> FileResponse:
	try:
		return FileResponse(open(settings.MEDIA_ROOT / file_name, 'rb'), as_attachment = True, filename = 'qrcode.jpg')
	except:
		return Http404('Файл не найден')