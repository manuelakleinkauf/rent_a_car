from django import forms
from django.core.exceptions import ValidationError
from .models import Vehicle, VehicleClass
import re

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'brand', 'model', 'year', 'color', 'km', 'vehicle_class', 'status', 'description', 'plate', 'image']
        labels = {
            'vehicle_type': 'Tipo de Veículo',
            'brand': 'Marca',
            'model': 'Modelo',
            'year': 'Ano',
            'color': 'Cor',
            'km': 'Quilometragem',
            'vehicle_class': 'Classe do Veículo',
            'status': 'Status',
            'description': 'Descrição',
            'plate': 'Placa',
            'image': 'Imagem do Veículo',
        }
        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'maxlength': '4', 'oninput': 'this.value=this.value.slice(0,4)'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'km': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vehicle_class': forms.Select(attrs={'class': 'form-control'}),
            'plate': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '7',
                'oninput': 'this.value = this.value.toUpperCase();',
                'pattern': '[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}',
                'title': 'Formato: ABC1D23 (3 letras, 1 número, 1 letra, 2 números)',}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

   
class VehicleClassForm(forms.ModelForm):
    class Meta:
        model = VehicleClass
        fields = ['name', 'description', 'daily_price']
        labels = {
            'name': 'Nome da Classe',
            'description': 'Descrição',
            'daily_price': 'Preço Diário',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'daily_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

