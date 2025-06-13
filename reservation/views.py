from django.shortcuts import render, redirect
from .models import Reservation
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ReservationForm
from django.shortcuts import get_object_or_404

# Create your views here.

def list_reservations(request):
    query = request.GET.get('search', '')
    sort = request.GET.get('sort', 'id')
    order = request.GET.get('order', 'asc')
    status = request.GET.get('status', '')
    sort_field = sort if order == 'asc' else f'-{sort}'

    if query:
        reservations = Reservation.objects.filter(
            Q(vehicle__plate__icontains=query) |
            Q(client__name__icontains=query)
        )
    else:
        reservations = Reservation.objects.all()

    if status:
        reservations = reservations.filter(status=status)

    reservations = reservations.order_by(sort_field)

    paginator = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    count = Reservation.objects.count()

    dados = {
        'total': count,
        'reservations': page_obj,
        'query': query,
        'sort': sort,
        'order': order,
        'page_obj': page_obj,
        'status': status,
    }

    return render(request, 'reservations/list_reservations.html', dados)

def reservation_detail(request, id):
    reservation = Reservation.objects.get(id=id)
    return render(request, 'reservations/reservation_detail.html', {
        'reservation': reservation,
    })

def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if start_date >= end_date:
                messages.error(request, "A data de início deve ser anterior à data de término.")
                return redirect('create_reservation')

            form.save()
            messages.success(request, "Reserva criada com sucesso.")
            return redirect('list_reservations')
    else:
        form = ReservationForm()
    
    return render(request, 'reservations/create_reservation.html', {'form': form})

def update_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if start_date >= end_date:
                messages.error(request, "A data de início deve ser anterior à data de término.")
                return redirect('update_reservation', id=id)
            form.save()
            messages.success(request, "Reserva atualizada com sucesso.")
            return redirect('list_reservations')
    else:
        form = ReservationForm(instance=reservation)
    
    return render(request, 'reservations/update_reservation.html', {'form': form})

def delete_reservation(request, id):
    reservation = Reservation.objects.get(id=id)
    if reservation.status == 'active':
        messages.error(request, "Não é possível excluir uma reserva ativa.")
        return redirect('list_reservations')
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Reserva excluída com sucesso.")
        return redirect('list_reservations')
    
    return render(request, 'reservations/delete.html', {'reservation': reservation})
