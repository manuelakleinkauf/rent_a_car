# Generated by Django 5.1.7 on 2025-06-26 21:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_delete_reservation'),
        ('reservation', '0002_alter_reservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', to='client.client'),
        ),
    ]
