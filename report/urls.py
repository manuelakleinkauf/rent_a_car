from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.report_index, name='report_index'),
    path('PDF', views.export_PDF, name='export_PDF'),
    path('excel', views.export_excel, name='export_excel'),
]