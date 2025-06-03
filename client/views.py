import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Client
from .forms import ClientForm

def client_list(request):
    query = request.GET.get('q', '').strip()  # Busca por nome ou CPF
    clients = Client.objects.all()

    if query:
        # Remove pontos, traços e espaços para buscar CPF sem formatação
        query_clean = re.sub(r'[\.\-\s]', '', query)

        clients = clients.filter(
            Q(name__icontains=query) |
            Q(cpf__icontains=query_clean)
        )
    return render(request, 'clients/list.html', {'clients': clients, 'query': query})

def client_detail(request, id):
    client = get_object_or_404(Client, id=id)
    active_reservations = client.reservations.filter(status='active')
    has_active_reservations = active_reservations.exists()
    return render(request, 'clients/detail.html', {
        'client': client,
        'active_reservations': active_reservations,
        'has_active_reservations': has_active_reservations,
    })

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente cadastrado com sucesso.")
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'clients/form.html', {'form': form})

def client_update(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente atualizado com sucesso.")
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/form.html', {'form': form})

def client_delete(request, id):
    client = get_object_or_404(Client, id=id)
    if client.active:  # aqui verifica se está ativo
        messages.error(request, "Não é possível excluir um cliente ativo. Por favor, inative antes de excluir.")
    elif client.reservations.filter(status='active').exists():
        messages.error(request, "Não é possível excluir. Cliente possui reservas ativas.")
    else:
        client.delete()
        messages.success(request, "Cliente excluído com sucesso.")
    return redirect('client_list')


def client_inactivate(request, id):
    client = get_object_or_404(Client, id=id)
    if client.reservations.filter(status='active').exists():
        messages.error(request, "Não é possível inativar. Cliente possui reservas ativas.")
    else:
        client.active = False
        client.save()
        messages.success(request, "Cliente inativado com sucesso.")
    return redirect('client_list')


