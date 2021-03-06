from django.db import models

import datetime


# Create your models here.
class leader(models.Model):
	surname = models.CharField('Фамилия', max_length = 255)
	name = models.CharField('Имя', max_length = 255)
	patronymic = models.CharField('Отчество', max_length = 255)
	login = models.CharField('Логин', max_length = 255)
	email = models.EmailField('Почта')
	passwd = models.CharField('Хеш пароля', max_length = 64)
	qrcode = models.FilePathField('Путь до QR кода')
	create_date = models.DateTimeField('Дата и время создания аккаунта', 
										default = datetime.datetime.now())

class college(models.Model):
	leader = models.ForeignKey(leader, on_delete = models.CASCADE)
	name = models.CharField('Название Колледжа', max_length = 255)
	create_date = models.DateTimeField('Дата и время создания аккаунта', 
										default = datetime.datetime.now())

class student(models.Model):
	college = models.ForeignKey(leader, on_delete = models.CASCADE)
	surname = models.CharField('Фамилия', max_length = 255)
	name = models.CharField('Имя', max_length = 255)
	patronymic = models.CharField('Отчество', max_length = 255)
	group = models.CharField('Группа', max_length = 255)
	qrcode = models.FilePathField('Путь до QR кода')
	create_date = models.DateTimeField('Дата и время создания аккаунта', 
										default = datetime.datetime.now())