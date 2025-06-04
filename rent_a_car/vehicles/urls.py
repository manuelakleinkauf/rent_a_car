from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_vehicles, name='list_vehicles'),
    path('criar/', views.create_vehicle, name='create_vehicle'),
    path('<int:vehicle_id>/', views.get_vehicle_by_id, name='vehicle_detail'),
    path('atualizar/<int:vehicle_id>/', views.update_vehicle, name='update_vehicle'),
    path('deletar/<int:vehicle_id>', views.delete_vehicle, name='delete_vehicle'),
    path('criar-classe/', views.create_vehicle_class, name='create_vehicle_class'),
    path('listar-classe/', views.list_vehicle_classes, name='list_vehicle_classes'),
    path('atualizar-classe/<int:vehicle_class_id>/', views.update_vehicle_class, name='update_vehicle_class'),
    path('deletar-classe/<int:vehicle_class_id>/', views.delete_vehicle_class, name='delete_vehicle_class'),
]