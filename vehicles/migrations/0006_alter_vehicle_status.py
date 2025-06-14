# Generated by Django 5.1.7 on 2025-06-13 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0005_vehicle_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='status',
            field=models.CharField(choices=[('available', 'Disponível'), ('rented', 'Alugado'), ('maintenance', 'Manutenção'), ('reserved', 'Reservado')], default='available', max_length=20),
        ),
    ]
