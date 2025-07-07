from django.urls import path
from . import views

urlpatterns = [
    path('', views.maintenance_list, name='maintenance_list'),
    path('create/', views.create_maintenance, name='create_maintenance'),
    path('complete/<int:maintenance_id>/', views.maintenance_complete, name='maintenance_complete'),
    path('<int:id>/editar_cliente/', views.maintenance_update, name='maintenance_update'),
     path('<int:id>/excluir_maintenance/', views.maintenance_delete, name='maintenance_delete'),
    path('<int:id>/', views.maintenance_detail, name='maintenance_detail'),
]
