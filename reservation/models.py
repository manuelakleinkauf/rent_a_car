from django.db import models

STATUS_CHOICES = [
('ativo', 'Ativo'),
('retirado', 'Retirado'),
('retornado', 'Retornado'),
('cancelado', 'Cancelado'),
]
# Create your models here.
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('returned', 'Retornado'),
        ('canceled', 'Cancelado'),
        ('picked_up', 'Retirado'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    vehicle = models.ForeignKey(
        'vehicles.Vehicle',
        on_delete=models.PROTECT,
    )
    client = models.ForeignKey(
        'client.Client',
        on_delete=models.PROTECT,
    )

    #retirada
    pickup_mileage = models.IntegerField(null=True, blank=True)
    pickup_fuel_level = models.CharField(max_length=20, null=True, blank=True)
    pickup_damage_notes = models.TextField(blank=True, null=True)

    #retorno
    return_mileage = models.IntegerField(null=True, blank=True)
    return_fuel_level = models.CharField(max_length=20, null=True, blank=True)
    return_damage_notes = models.TextField(blank=True, null=True)