from django.db import models
from vehicles.models import Vehicle
from django.utils import timezone

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

    @property
    def is_active(self):
        return not self.completed
