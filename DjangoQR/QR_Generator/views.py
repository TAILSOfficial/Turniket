from django.http import HttpResponse, Http404
# from cryptography.fernet import Fernet
from django.shortcuts import render
from django.conf import settings

import qrcode
import os


def numerator() -> int:
    i = 0
    while True:
        yield i
        i += 1
num = numerator()
for i in os.listdir(settings.IMAGE_PATH):
    next(num)


def gen_qr_code(name: str, group: str, **bruh) -> str:
    # cipher = Fernet(key[0].encode('utf-8'))
    # data = cipher.encrypt((name[0] + ', ' + group[0]).encode('utf-8')).decode('utf-8')
    data = name[0] + ', ' + group[0]
    img = qrcode.make(data)

    if getattr(settings, 'SAVE_IMAGE'):
        img.save(settings.IMAGE_PATH / f'{data}.jpg')

    return data + '.jpg'

def index(request):
    if request.method == 'POST':
        data = gen_qr_code(**request.POST)

        return render(request, 'qr_generator.html', {
            'is_post': request.method == 'POST',
            'data': data})

    else:
       return render(request, 'qr_generator.html', {
            'is_post': request.method == 'POST'}) 