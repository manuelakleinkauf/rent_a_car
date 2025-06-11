from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),  
    path('cadastrar_funcionario/', views.employee_create, name='employee_create'),
    path('<int:id>/', views.employee_detail, name='employee_detail'),
    path('<int:id>/editar_funcionario/', views.employee_update, name='employee_update'),
    path('<int:id>/excluir_funcionario/', views.employee_delete, name='employee_delete'),
    path('<int:id>/inativar_funcionario/', views.employee_inactivate, name='employee_inactivate'),
]
