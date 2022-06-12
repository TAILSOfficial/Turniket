from django.urls import path

from . import views


urlpatterns = [
	path('<str: college_name>/', views.view),
]