from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('current', views.index, name='current'),
    path('forecast', views.forecast, name='forecast'),
    path('about', views.about, name='about'),
]
