from django import forms
from .models import Reservation

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
            'status': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '7',
                'oninput': 'this.value = this.value.toUpperCase();',
                'pattern': '[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}',
                'title': 'Formato: ABC1D23 (3 letras, 1 número, 1 letra, 2 números)',}),
            'client': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
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
