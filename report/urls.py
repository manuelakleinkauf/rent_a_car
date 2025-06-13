from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.report_index, name='report_index'),
]