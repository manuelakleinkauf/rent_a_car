from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_vehicles, name='list_vehicles'),
    path('criar/', views.create_vehicle, name='create_vehicle'),
    path('<int:vehicle_id>/', views.get_vehicle_by_id, name='vehicle_detail'),
    path('atualizar/<int:vehicle_id>/', views.update_vehicle, name='update_vehicle'),
]