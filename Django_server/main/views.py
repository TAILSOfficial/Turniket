from django.http import HttpResponseRedirect as hrr
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from hashlib import sha256

from . import models


def index(request):
	leader = None

	if 'ID' in request.COOKIES:
		leader = models.leader.objects.get(id = request.COOKIES['ID'])

	return render(request, 'index.html', {'leader': leader});

def login(request):
	if request.method == 'POST':
		user = authenticate(request, username=request.POST['login'], password=request.POST['password'])
		# for obj in models.leader.objects.all():
		# 	if obj.login == request.POST['login'] and obj.passwd == sha256(request.POST['password'].encode('utf-8')):
		# 		responce = hrr('/')
		# 		responce.set_cookie("ID", obj.id)

		# 		return responce;
		print(user)
		print(dir(user))
		return render(request, 'login.html', {'NF': True});

	else:
		return render(request, 'login.html', {'NF': False});