from django.urls import path

from . import views


urlpatterns = [
	path('0/', views.cam0, name = 'Cam0'),
	path('1/', views.cam1, name = 'Cam1'),
]