from django.shortcuts import render, get_object_or_404, redirect
from .models import Maintenance
from vehicles.models import Vehicle
from .forms import MaintenanceForm
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def create_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.save()
            messages.success(request, "Manutenção registrada com sucesso.")
            return redirect('maintenance_list')
        else:
            messages.error(request, "Erro ao registrar manutenção. Verifique os dados.")
    else:
        form = MaintenanceForm()

    return render(request, 'maintenance/create.html', {'form': form})

@login_required
def maintenance_complete(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, id=maintenance_id)

    if not maintenance.completed:
        maintenance.completed = True
        maintenance.save()  

    return redirect('maintenance_list')

@login_required
def maintenance_list(request):
    search_query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'start_date')  
    order = request.GET.get('order', 'desc')      

    maintenance_list = Maintenance.objects.select_related('vehicle')

    if search_query:
        maintenance_list = maintenance_list.filter(
            vehicle__plate__icontains=search_query
        )

    ordering = sort if order == 'asc' else f'-{sort}'
    maintenance_list = maintenance_list.order_by(ordering)

    paginator = Paginator(maintenance_list, 10)
    page_number = request.GET.get('page')
    maintenances = paginator.get_page(page_number)

    return render(request, 'maintenance/list.html', {
        'maintenances': maintenances,
        'search_query': search_query,
        'sort': sort,
        'order': order,
    })

@login_required
def maintenance_update(request, id):
    maintenance = get_object_or_404(Maintenance, id=id)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            maintenance = form.save()

            # Atualiza o status do veículo com base no campo "completed"
            if maintenance.completed:
                maintenance.vehicle.status = 'disponível'
            else:
                maintenance.vehicle.status = 'em manutenção'
            maintenance.vehicle.save()

            messages.success(request, "Manutenção atualizada com sucesso.")
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm(instance=maintenance)
    return render(request, 'maintenance/update.html', {'form': form})


@login_required
def maintenance_detail(request, id):
    maintenance = get_object_or_404(Maintenance, id=id)
    return render(request, 'maintenance/detail.html', {'maintenance': maintenance})

@login_required
def maintenance_delete(request, id):
    maintenance = get_object_or_404(Maintenance, id=id)
    
    if not maintenance.completed:
        messages.error(request, "Não é possível excluir uma manutenção em andamento. Finalize antes de excluir.")
    else:
        maintenance.delete()
        messages.success(request, "Manutenção excluída com sucesso.")
    
    return redirect('maintenance_list')