from django import forms
from .models import Maintenance, STATUS_CHOICES
from vehicles.models import Vehicle

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['vehicle', 'reason', 'expected_end_date']
        labels = {
            'vehicle': 'Veículo',
            'reason': 'Motivo',
            'expected_end_date': 'Previsão de Conclusão',
        }
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'expected_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, show_status=False, **kwargs):
     super().__init__(*args, **kwargs)

     if self.instance.pk:
        # Modo edição: desabilita o campo 'vehicle' (já está vinculado à manutenção)
        self.fields['vehicle'].disabled = True
     else:
        # Modo criação: exibe apenas veículos disponíveis
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status='available')

     if show_status:
        self.fields['status'] = forms.ChoiceField(
            choices=STATUS_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Status'
        )

    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        if vehicle and vehicle.status != 'available':
            raise forms.ValidationError("Veículo não está disponível para manutenção.")
        return cleaned_data
