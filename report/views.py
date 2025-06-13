from django.shortcuts import render
from reservation.models import Reservation
from vehicles.models import Vehicle
from client.models import Client
from employee.models import Employee
# Create your views here.

def report_index(request):
    total_vehicles = Vehicle.objects.count()
    available_vehicles = Vehicle.objects.filter(status='available').count()

    if total_vehicles > 0:
        available_percent = int((available_vehicles / total_vehicles) * 100)
    else:
        available_percent = 0

    data = {
        'active_clients': Client.objects.filter(active=True).count(),
        'inactive_clients': Client.objects.filter(active=False).count(),
        'total_vehicles': total_vehicles,
        'available_vehicles': available_vehicles,
        'available_percent': available_percent, 
        'total_reservations': Reservation.objects.count(),
        'active_reservations': Reservation.objects.filter(status='active').count(),
        'completed_reservations': Reservation.objects.filter(status='completed').count(),
        'canceled_reservations': Reservation.objects.filter(status='canceled').count(),
        'total_employees': Employee.objects.count(),
        'active_employees': Employee.objects.filter(active=True).count(),
        'inactive_employees': Employee.objects.filter(active=False).count(),
    }
    return render(request, 'reports/index.html', data)