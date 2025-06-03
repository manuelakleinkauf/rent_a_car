from django.contrib import admin
from .models import Vehicle, VehicleClass

# Register your models here.
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_type', 'brand', 'model', 'year', 'color', 'km', 'vehicle_class', 'status')
    search_fields = ('brand', 'model')
    list_filter = ('vehicle_type', 'status')
    ordering = ('-created_at',)

@admin.register(VehicleClass)
class VehicleClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'daily_price')
    search_fields = ('name',)
    ordering = ('name',)