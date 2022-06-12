from django.db import models

import datetime


# Create your models here.
class leader(models.Model):
	college = models.CharField('Колледж', max_length = 255)
	surname = models.CharField('Фамилия', max_length = 255)
	name = models.CharField('Имя', max_length = 255)
	patronymic = models.CharField('Отчество', max_length = 255)
	login = models.CharField('Логин', max_length = 255)
	email = models.EmailField('Почта')
	passwd = models.CharField('Хеш пароля', max_length = 64)
	qrcode = models.FilePathField('Путь до QR кода')
	create_date = models.DateTimeField('Дата и время создания аккаунта', 
										default = datetime.datetime.now())

	def __str__(self) -> str:
		return self.surname.title() + ' ' + self.name[0].upper() + '. ' + self.patronymic[0].upper() + '.'

class member(models.Model):
	leader = models.ForeignKey(leader, on_delete = models.CASCADE)
	college = models.CharField('Колледж', max_length = 255)
	surname = models.CharField('Фамилия', max_length = 255)
	name = models.CharField('Имя', max_length = 255)
	patronymic = models.CharField('Отчество', max_length = 255)
	group = models.CharField('Группа', max_length = 255)
	qrcode = models.FilePathField('Путь до QR кода')
	create_date = models.DateTimeField('Дата и время создания аккаунта', 
										default = datetime.datetime.now())

	def __str__(self) -> str:
		return self.surname.title() + ' ' + self.name[0].upper() + '. ' + self.patronymic[0].upper() + '.'

class INFO(models.Model):
	college = models.CharField('Колледж', max_length = 255)
	fio = models.CharField('ф. И. О.', max_length = 255)
	date_time = models.DateTimeField('Время прохождения')
	photo = models.FilePathField('Путь до снимка')
	qrcode = models.FilePathField('Путь до QR кода')