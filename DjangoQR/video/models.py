from django.db import models

# Create your models here.
class enter(models.Model):
	id = models.AutoField('Идентификатор', primary_key = True)
	group = models.CharField('Группа', max_length = 90)
	name = models.CharField('Ф. И. О.', max_length = 255)
	path_to_img = models.FilePathField('Путь до Изображения с камеры')
	date = models.DateTimeField('Дата и время', auto_now_add = True)

	def __str__(self) -> str:
		return f'{self.name}, {self.group}'

	class Meta:
		verbose_name = 'Инфо о прохождении'
		verbose_name_plural = 'Инфо о прохождениях'

class data(models.Model):
	id = models.AutoField('Идентификатор', primary_key = True)
	group = models.CharField('Группа', max_length = 90)
	name = models.CharField('Ф. И. О.', max_length = 255)

	@classmethod
	def users_dict(cls) -> dict[str, str]:
		return {a.name: a.group for a in cls.objects.all()}

	def __str__(self) -> str:
		return f'{self.name} {self.group}'

	class Meta:
		verbose_name = 'Состав'
		verbose_name_plural = 'Список состава'