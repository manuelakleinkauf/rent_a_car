from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_maintenance, name='maintenance_list'),
    path('create/<int:vehicle_id>/', views.create_maintenance, name='create_maintenance'),
    path('complete/<int:maintenance_id>/', views.complete_maintenance, name='maintenance_complete'),
]
