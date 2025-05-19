from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'brand', 'model', 'year', 'color', 'km', 'price_per_day', 'status', 'description']
        labels = {
            'vehicle_type': 'Tipo de Veículo',
            'brand': 'Marca',
            'model': 'Modelo',
            'year': 'Ano',
            'color': 'Cor',
            'km': 'Quilometragem',
            'price_per_day': 'Preço por Dia (R$)',
            'status': 'Status',
            'description': 'Descrição',
        }

        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'km': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
