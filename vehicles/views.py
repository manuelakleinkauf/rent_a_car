from django.shortcuts import render
from django.shortcuts import redirect
from .forms import VehicleForm
from django.shortcuts import get_object_or_404
from .models import Vehicle
# Create your views here.

def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_vehicles')
    else:
        form = VehicleForm()
    
    dados = {
        'form': form,
    }
    return render(request, 'vehicles/create_vehicle.html', dados)

def list_vehicles(request):
    vehicles = Vehicle.objects.all()
    dados = {
        'vehicles': vehicles,
    }
    return render(request, 'vehicles/list_vehicles.html', dados)

def get_vehicle_by_id(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    dados = {
        'vehicle': vehicle,
    }
    return render(request, 'vehicles/vehicle_detail.html', dados)

def update_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('list_vehicles')
    else:
        form = VehicleForm(instance=vehicle)
    dados = {
        'form': form,
        'vehicle': vehicle,
    }
    return render(request, 'vehicles/update_vehicle.html', dados)