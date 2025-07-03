from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ReservationForm
from .forms import PickupForm, ReturnForm
from django.contrib.auth.decorators import login_required

@login_required
def list_reservations(request):
    query = request.GET.get('search', '')
    sort = request.GET.get('sort', 'id')
    order = request.GET.get('order', 'asc')
    status = request.GET.get('status', '')

    sort_field = sort if order == 'asc' else f'-{sort}'

    reservations = Reservation.objects.all()

    if query:
        reservations = reservations.filter(
            Q(vehicle__plate__icontains=query) |
            Q(client__name__icontains=query)
        )

    if status:
        reservations = reservations.filter(status=status)

    reservations = reservations.order_by(sort_field)
    paginator = Paginator(reservations, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'total': reservations.count(),
        'reservations': page_obj,
        'query': query,
        'sort': sort,
        'order': order,
        'page_obj': page_obj,
        'status': status,
    }
    return render(request, 'reservations/list_reservations.html', context)

@login_required
def reservation_detail(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    return render(request, 'reservations/reservation_detail.html', {'reservation': reservation})

@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)

            if reservation.start_date >= reservation.end_date:
                messages.error(request, "A data de início deve ser anterior à data de término.")
                return redirect('create_reservation')

            if reservation.vehicle.status != 'available':
                messages.error(request, "O veículo selecionado não está disponível.")
                return redirect('create_reservation')

            reservation.save()

            if reservation.status == 'active':
                reservation.vehicle.status = 'reserved'
            elif reservation.status == 'picked_up':
                reservation.vehicle.status = 'rented'
            else:
                reservation.vehicle.status = 'available'

            reservation.vehicle.save()

            messages.success(request, "Reserva criada com sucesso.")
            return redirect('list_reservations')
    else:
        form = ReservationForm()

    return render(request, 'reservations/create_reservation.html', {'form': form})

@login_required
def update_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    original_vehicle = reservation.vehicle
    original_status = reservation.status

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            updated = form.save(commit=False)

            if updated.start_date >= updated.end_date:
                messages.error(request, "A data de início deve ser anterior à data de término.")
                return redirect('update_reservation', id=id)

            new_vehicle = updated.vehicle
            new_status = updated.status

            if new_vehicle != original_vehicle:
                if new_vehicle.status != 'available':
                    messages.error(request, "O novo veículo selecionado não está disponível.")
                    return redirect('update_reservation', id=id)

                if original_status in ['active', 'picked_up']:
                    original_vehicle.status = 'available'
                    original_vehicle.save()

                if new_status == 'active':
                    new_vehicle.status = 'reserved'
                elif new_status == 'picked_up':
                    new_vehicle.status = 'rented'
                else:
                    new_vehicle.status = 'available'

                new_vehicle.save()

            else:
                if original_status != new_status:
                    if new_status in ['returned', 'canceled']:
                        new_vehicle.status = 'available'
                    elif new_status == 'active':
                        new_vehicle.status = 'reserved'
                    elif new_status == 'picked_up':
                        new_vehicle.status = 'rented'
                    new_vehicle.save()

            updated.save()
            messages.success(request, "Reserva atualizada com sucesso.")
            return redirect('list_reservations')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservations/update_reservation.html', {
        'form': form,
        'reservation': reservation
    })

@login_required
def delete_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    print(reservation.status)
    if reservation.status == 'active' or reservation.status == 'picked_up':
        messages.error(request, "Não é possível excluir uma reserva ativa ou retirada.")
        return redirect('list_reservations')

    if request.method == 'POST':
        vehicle = reservation.vehicle

        if reservation.status in ['active', 'picked_up']:
            vehicle.status = 'available'
            vehicle.save()

        reservation.delete()
        messages.success(request, "Reserva excluída com sucesso.")
        return redirect('list_reservations')

    return render(request, 'reservations/delete.html', {'reservation': reservation})

@login_required
def create_pickup(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    if reservation.status != 'active' and reservation.status != 'ativo':
        messages.error(request, "A reserva deve estar ativa para registrar a retirada.")
        return redirect('list_reservations')
    
    if request.method == 'POST':
        form = PickupForm(request.POST)
        if form.is_valid():
            reservation.pickup_mileage = form.cleaned_data['pickup_mileage']
            reservation.pickup_fuel_level = form.cleaned_data['pickup_fuel_level']
            reservation.pickup_damage_notes = form.cleaned_data['pickup_damage_notes']
            reservation.status = 'picked_up'
            vehicle = reservation.vehicle
            vehicle.status = 'rented'
            vehicle.save()
            reservation.save()

            messages.success(request, "Retirada registrada com sucesso.")
            return redirect('list_reservations')
    else:
        form = PickupForm()

    return render(request, 'reservations/create_pickup.html', {'form': form, 'reservation': reservation})

@login_required
def create_return(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    
    rented_days = (reservation.end_date - reservation.start_date).days
    amount_due = rented_days * reservation.vehicle.vehicle_class.daily_price
    amount_due = round(amount_due, 2)

    if reservation.status != 'picked_up':
        messages.error(request, "A reserva deve estar retirada para registrar o retorno.")
        return redirect('list_reservations')
    
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            reservation.return_mileage = form.cleaned_data['return_mileage']
            reservation.return_fuel_level = form.cleaned_data['return_fuel_level']
            reservation.return_damage_notes = form.cleaned_data['return_damage_notes']
            
            reservation.status = 'returned'
            reservation.vehicle.status = 'available'
            
            reservation.vehicle.save()
            reservation.save()

            messages.success(request, "Informações de retorno salvas com sucesso.")
            return redirect('list_reservations')
    else:
        form = ReturnForm()

    return render(request, 'reservations/create_return.html', {
        'form': form,
        'reservation': reservation,
        'amount_due': amount_due,
    })
