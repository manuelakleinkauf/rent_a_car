from django.db import models
from django.core.exceptions import ValidationError


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    email = models.EmailField(verbose_name="E-mail")
    address = models.TextField(blank=True, null=True, verbose_name="Endereço")
    phone = models.CharField(max_length=11, verbose_name="Telefone")
    active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def clean(self):
        # Valida CPF só com dígitos e tamanho 11
        if not self.cpf.isdigit() or len(self.cpf) != 11:
            raise ValidationError(
                "CPF inválido. Deve conter exatamente 11 dígitos.")
        # Valida telefone só com dígitos e tamanho 11
        if not self.phone.isdigit() or len(self.phone) != 11:
            raise ValidationError(
                "Telefone deve conter 11 dígitos, incluindo DDD.")

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
                "Cliente possui reservas ativas e não pode ser inativado.")
        self.active = False
        self.save()

    @property
    def cpf_formatado(self):
        # Formata o CPF como 123.456.789-00
        cpf = self.cpf
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    @property
    def phone_formatado(self):
        # Supondo que phone tem 11 dígitos: DDD + número (ex: 51976328951)
        if len(self.phone) == 11:
            ddd = self.phone[:2]
            parte1 = self.phone[2:7]
            parte2 = self.phone[7:]
            return f"({ddd}) {parte1}-{parte2}"
        return self.phone  # se não tiver 11 dígitos, retorna como está

