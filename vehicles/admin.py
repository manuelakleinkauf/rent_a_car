from django.contrib import admin
from .models import Vehicle

# Register your models here.
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_type', 'brand', 'model', 'year', 'color', 'km', 'price_per_day', 'status')
    search_fields = ('brand', 'model')
    list_filter = ('vehicle_type', 'status')
    ordering = ('-created_at',)
