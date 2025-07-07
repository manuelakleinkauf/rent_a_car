from django.db import models
from vehicles.models import Vehicle
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

STATUS_CHOICES = (
    ('in_progress', 'Em Manutenção'),
    ('completed', 'Concluída'),
)

class Maintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenances')
    reason = models.TextField()
    expected_end_date = models.DateField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

    def __str__(self):
        return f"Manutenção - {self.vehicle.plate} ({'Concluída' if self.completed else 'Em andamento'})"

    def save(self, *args, **kwargs):
        if self.completed:
            self.status = 'completed'
            self.end_date = self.end_date or timezone.now()
            self.vehicle.status = 'available'
        else:
            self.status = 'in_progress'
            self.vehicle.status = 'maintenance'
        self.vehicle.save()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.expected_end_date and self.start_date:
            max_end_date = self.start_date.date() + timedelta(days=30)
            if self.expected_end_date > max_end_date:
                raise ValidationError({
                    'expected_end_date': 'A data prevista para término não pode ser maior que 30 dias após o início da manutenção.'
                })
    @property
    def is_active(self):
        return not self.completed
