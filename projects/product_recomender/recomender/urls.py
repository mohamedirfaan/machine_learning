from django.contrib import admin
from django.urls import include
from soulmates import routing
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name="home"),
]