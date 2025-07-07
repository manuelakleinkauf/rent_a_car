from django.db import models
from django.core.exceptions import ValidationError

POSITIONS_CHOICES = (
    ('admin', 'Administrador'),
    ('secretary', 'Secretária'),
    ('manager', 'Gerente'),
    ('seller', 'Vendedor')
)

class Employee(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    email = models.EmailField(verbose_name="E-mail")
    address = models.TextField(blank=True, null=True, verbose_name="Endereço")
    phone = models.CharField(max_length=11, verbose_name="Telefone")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    position = models.CharField(
        max_length=20, choices=POSITIONS_CHOICES, default='')

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.cpf})"

    def has_active_reservations(self):
        return self.reservations.filter(status='active').exists()

    def deactivate(self):
        if self.has_active_reservations():
            raise ValidationError(
                "Funcionário possui reservas ativas e não pode ser inativado.")
        self.active = False
        self.save()

    @property
    def cpf_formatado(self):
        cpf = self.cpf
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    @property
    def phone_formatado(self):
        if len(self.phone) == 11:
            ddd = self.phone[:2]
            parte1 = self.phone[2:7]
            parte2 = self.phone[7:]
            return f"({ddd}) {parte1}-{parte2}"
        return self.phone  


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('completed', 'Concluída'),
        ('cancelled', 'Cancelada'),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-reservation_date']

    def __str__(self):
        return f"Reserva de {self.employee.name} em {self.reservation_date.strftime('%d/%m/%Y %H:%M')} - {self.status}"
