from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.report_index, name='report_index'),
    path('PDF', views.export_PDF, name='export_PDF'),
    path('excel', views.export_excel, name='export_excel'),
    path('client', views.client_historic_report, name='client_historic_report'),
    path('client/PDF', views.export_client_historic_report_pdf, name='export_client_historic_report_pdf'),
    path('client/excel', views.export_client_historic_report_excel, name='export_client_historic_report_excel'),
]