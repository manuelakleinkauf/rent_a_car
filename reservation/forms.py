from django import forms
from .models import Reservation
from vehicles.models import Vehicle

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['client', 'vehicle', 'start_date', 'end_date', 'status' ]
        labels = {
            'status': 'Status',
            'start_date': 'Data de Início',
            'end_date': 'Data de Término',
            'vehicle': 'Veículo',
            'client': 'Cliente',
        }
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control no-arrow'}),
        }


    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)

        self.fields['vehicle'].queryset = Vehicle.objects.exclude(status='maintenance') 
        
        for field in ['start_date', 'end_date']:
            if self.instance and getattr(self.instance, field):
                self.fields[field].initial = getattr(self.instance, field).strftime('%Y-%m-%d')

class PickupForm(forms.Form):
    pickup_mileage = forms.IntegerField(label="Quilometragem de Retirada")
    pickup_fuel_level = forms.CharField(label="Nível de Combustível na Retirada")
    pickup_damage_notes = forms.CharField(
        label="Observações sobre Danos na Retirada",
        widget=forms.Textarea,
        required=False
    )

class ReturnForm(forms.Form):
    return_mileage = forms.IntegerField(label="Quilometragem de Retorno")
    return_fuel_level = forms.CharField(label="Nível de Combustível no Retorno")
    return_damage_notes = forms.CharField(
        label="Observações sobre Danos no Retorno",
        widget=forms.Textarea,
        required=False
    )

