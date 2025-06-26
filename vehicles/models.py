from django.db import models

# Create your models here.
VEHICLE_TYPE_CHOICES = (
    ('car', 'Carro'),
    ('motorcycle', 'Moto'),
    ('truck', 'Caminhão'),
)

VEHICLE_BRAND_CHOICES = (
    ('toyota', 'Toyota'),
    ('honda', 'Honda'),
    ('ford', 'Ford'),
    ('chevrolet', 'Chevrolet'),
    ('bmw', 'BMW'),
)

STATUS_CHOICES = (
    ('available', 'Disponível'),
    ('rented', 'Alugado'),
    ('maintenance', 'Manutenção'),
    ('reserved', 'Reservado'),
)

class VehicleClass(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)
    brand = models.CharField(max_length=20, choices=VEHICLE_BRAND_CHOICES)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    km = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    plate = models.CharField(max_length=7, unique=True, default='')
    vehicle_class = models.ForeignKey(VehicleClass, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='vehicles/images/', blank=True, null=True)
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"