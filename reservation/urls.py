from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.list_reservations, name='list_reservations'),
    path('<int:id>/', views.reservation_detail, name='reservation_detail'),
    path('create/', views.create_reservation, name='create_reservation'),
    path('update/<int:id>/', views.update_reservation, name='update_reservation'),
    path('delete/<int:id>/', views.delete_reservation, name='delete_reservation'),
    path('pickup/<int:id>/', views.create_pickup, name='create_pickup'),
    path('return/<int:id>/', views.create_return, name='create_return'),
]