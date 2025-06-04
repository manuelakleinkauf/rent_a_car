from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list, name='client_list'),  # Lista de clientes em /client/
    path('cadastrar_cliente/', views.client_create, name='client_create'),
    path('<int:id>/', views.client_detail, name='client_detail'),
    path('<int:id>/editar_cliente/', views.client_update, name='client_update'),
    path('<int:id>/excluir_cliente/', views.client_delete, name='client_delete'),
    path('<int:id>/inativar_cliente/', views.client_inactivate, name='client_inactivate'),
]
