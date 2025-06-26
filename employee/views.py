import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Employee
from .forms import EmployeeForm
from django.core.paginator import Paginator


def employee_list(request):
    query = request.GET.get('q', '').strip()  
    employees = Employee.objects.all()
    sort = request.GET.get('sort', 'id')
    order = request.GET.get('order', 'asc')

    if query:
        query_clean = re.sub(r'[\.\-\s]', '', query)

        employees = employees.filter(
            Q(name__icontains=query) |
            Q(cpf__icontains=query_clean)
        )

    if order == 'desc':
        sort = '-' + sort
    employees = employees.order_by(sort)

    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    employees = paginator.get_page(page_number)

    count = Employee.objects.count()
    return render(request, 'employees/list.html', {'employees': employees, 'query': query, 'sort': sort, 'order': order, 'total': count, 'page_range': paginator.page_range})


def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)
    active_reservations = employee.reservations.filter(status='active')
    has_active_reservations = active_reservations.exists()
    return render(request, 'employees/detail.html', {
        'employee': employee,
        'active_reservations': active_reservations,
        'has_active_reservations': has_active_reservations,
    })


def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário cadastrado com sucesso.")
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/form.html', {'form': form})


def employee_update(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário atualizado com sucesso.")
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/update.html', {'form': form})


def employee_delete(request, id):
    employee = get_object_or_404(Employee, id=id)
    if employee.active:  
        messages.error(
            request, "Não é possível excluir um funcionário ativo. Por favor, inative antes de excluir.")
    elif employee.reservations.filter(status='active').exists():
        messages.error(
            request, "Não é possível excluir. Funcionário possui reservas ativas.")
    else:
        employee.delete()
        messages.success(request, "Funcionário excluído com sucesso.")
    return redirect('employee_list')


def employee_inactivate(request, id):
    employee = get_object_or_404(Employee, id=id)
    if employee.reservations.filter(status='active').exists():
        messages.error(
            request, "Não é possível inativar. Funcionário possui reservas ativas.")
    else:
        employee.active = False
        employee.save()
        messages.success(request, "Funcionário inativado com sucesso.")
    return redirect('employee_list')
