from django.shortcuts import render, get_object_or_404, redirect
from .models import Maintenance
from vehicles.models import Vehicle
from .forms import MaintenanceForm
from django.core.paginator import Paginator
from django.utils import timezone


def create_maintenance(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)


    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.vehicle = vehicle
            maintenance.save()


            vehicle.status = 'maintenance'
            vehicle.save()


            return redirect('list_maintenance')
    else:
        form = MaintenanceForm()


    return render(request, 'maintenance/form.html', {'form': form})


def complete_maintenance(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, id=maintenance_id)
    maintenance.completed = True
    maintenance.end_date = timezone.now()
    maintenance.save()


    maintenance.vehicle.status = 'available'
    maintenance.vehicle.save()


    return redirect('maintenance_list')




def list_maintenance(request):
    maintenance_list = Maintenance.objects.select_related('vehicle').order_by('-start_date')
    paginator = Paginator(maintenance_list, 10)  # 10 por página


    page_number = request.GET.get('page')
    maintenances = paginator.get_page(page_number)


    return render(request, 'maintenance/list.html', {'maintenances': maintenances})






