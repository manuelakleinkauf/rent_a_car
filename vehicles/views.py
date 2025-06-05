from django.shortcuts import render
from django.shortcuts import redirect
from .forms import VehicleForm, VehicleClassForm
from django.shortcuts import get_object_or_404
from .models import Vehicle, VehicleClass
from django.contrib import messages
# Create your views here.

def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_vehicles')
    else:
        form = VehicleForm()
    
    dados = {
        'form': form,
    }
    return render(request, 'vehicles/create_vehicle.html', dados)

def index(request):
    query = request.GET.get('search', '')
    if query:
        vehicles = Vehicle.objects.filter(plate__icontains=query, status='available') | Vehicle.objects.filter(model__icontains=query, status='available')
    else:
        vehicles = Vehicle.objects.filter(status='available')
    count = Vehicle.objects.count()
    dados = {
        'total': count,
        'vehicles': vehicles,
        'query': query,
    }
    return render(request, 'vehicles/index.html', dados)

def list_vehicles(request):
    query = request.GET.get('search', '')
    count = Vehicle.objects.count()
    if query:
        vehicles = Vehicle.objects.filter(plate__icontains=query) | Vehicle.objects.filter(model__icontains=query)
    else:
        vehicles = Vehicle.objects.all()
    dados = {
        'total': count,
        'vehicles': vehicles,
        'query': query,
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
        form = VehicleForm(request.POST, instance=vehicle, files=request.FILES)
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

def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if vehicle.status == 'rented':
        messages.error(request, 'Veículo alugado não pode ser deletado!')
        return redirect('list_vehicles')
    vehicle.delete()
    messages.success(request, 'Veículo deletado com sucesso!')
    return redirect('list_vehicles')

def create_vehicle_class(request):
    if request.method == 'POST':
        form = VehicleClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_vehicle_classes')
    else:
        form = VehicleClassForm()
    
    dados = {
        'form': form,
    }
    return render(request, 'vehicle_class/create_vehicle_class.html', dados)

def update_vehicle_class(request, vehicle_class_id):
    vehicle_class = VehicleClass.objects.get(id=vehicle_class_id)
    if request.method == 'POST':
        form = VehicleClassForm(request.POST, instance=vehicle_class)
        if form.is_valid():
            form.save()
            return redirect('list_vehicle_classes')
    else:
        form = VehicleClassForm(instance=vehicle_class)
    dados = {
        'form': form,
        'vehicle_class': vehicle_class,
    }
    return render(request, 'vehicle_class/update_vehicle_class.html', dados)

def list_vehicle_classes(request):
    query = request.GET.get('search', '')
    if query:
        vehicle_classes = VehicleClass.objects.filter(name__icontains=query)
    else:
        vehicle_classes = VehicleClass.objects.all()
    count = vehicle_classes.count()
    dados = {
        'vehicle_classes': vehicle_classes,
        'total': count,
        'query': query,
    }
    return render(request, 'vehicle_class/list_vehicle_classes.html', dados)
    
def delete_vehicle_class(request, vehicle_class_id):
    vehicle_class = get_object_or_404(VehicleClass, id=vehicle_class_id)
    if vehicle_class.vehicle_set.exists():
        messages.error(request, 'Classe de veículo não pode ser deletada pois possui veículos associados!')
        return redirect('list_vehicle_classes')
    vehicle_class.delete()
    messages.success(request, 'Classe de veículo deletada com sucesso!')
    return redirect('list_vehicle_classes')

