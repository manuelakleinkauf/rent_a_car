from django.shortcuts import render
from reservation.models import Reservation
from vehicles.models import Vehicle
from client.models import Client
from employee.models import Employee
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from openpyxl import Workbook
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

def export_PDF(request):
    total_vehicles = Vehicle.objects.count()
    available_vehicles = Vehicle.objects.filter(status='available').count()

    if total_vehicles > 0:
        available_percent = int((available_vehicles / total_vehicles) * 100)
    else:
        available_percent = 0

    data = {
        'Clientes Ativos': Client.objects.filter(active=True).count(),
        'Clientes Inativos': Client.objects.filter(active=False).count(),
        'Total de Veiculos': total_vehicles,
        'Veiculos Disponiveis': available_vehicles,
        'Percentual Disponivel': f'{available_percent}%',
        'Total de Reservas': Reservation.objects.count(),
        'Reservas Ativas': Reservation.objects.filter(status='active').count(),
        'Reservas Completas': Reservation.objects.filter(status='completed').count(),
        'Reservas Canceladas': Reservation.objects.filter(status='canceled').count(),
        'Total de Funcionarios': Employee.objects.count(),
        'Funcionarios Ativos': Employee.objects.filter(active=True).count(),
        'Funcionarios Inativos': Employee.objects.filter(active=False).count(),
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(width / 2, height - 50, "Relatorio Geral")

    y = height - 100

    pdf.setFont("Helvetica", 12)
    for key, value in data.items():
        pdf.drawString(50, y, f"{key}: {value}")
        y -= 20
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = height - 50

    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(50, 30, "Rent a Car")

    pdf.showPage()
    pdf.save()

    return response


def export_excel(request):
    total_vehicles = Vehicle.objects.count()
    available_vehicles = Vehicle.objects.filter(status='available').count()
    available_percent = int((available_vehicles / total_vehicles) * 100) if total_vehicles > 0 else 0

    data = {
        'Clientes Ativos': Client.objects.filter(active=True).count(),
        'Clientes Inativos': Client.objects.filter(active=False).count(),
        'Veículos Totais': total_vehicles,
        'Veículos Disponíveis': available_vehicles,
        'Disponibilidade atual de veículos (%)': available_percent,
        'Reservas Totais': Reservation.objects.count(),
        'Reservas Ativas': Reservation.objects.filter(status='active').count(),
        'Reservas Concluídas': Reservation.objects.filter(status='completed').count(),
        'Reservas Canceladas': Reservation.objects.filter(status='canceled').count(),
        'Funcionários Totais': Employee.objects.count(),
        'Funcionários Ativos': Employee.objects.filter(active=True).count(),
        'Funcionários Inativos': Employee.objects.filter(active=False).count(),
    }

    wb = Workbook()
    ws = wb.active
    ws.title = "Relatório Geral"

    ws.append(["Descrição", "Quantidade"])

    for key, value in data.items():
        ws.append([key, value])

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="relatorio_dashboard.xlsx"'
    wb.save(response)
    return response