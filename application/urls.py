from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^close_villages$', views.from_click, name='from_click'),
    url(r'^colonise$', views.colonise, name='colonise'),
]
