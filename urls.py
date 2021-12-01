from django.urls import path
from . import views

app_name = 'sbm'

urlpatterns = [
	path('', views.index, name='index'),
]
