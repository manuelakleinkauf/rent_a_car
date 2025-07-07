from django import forms
from .models import Maintenance, STATUS_CHOICES
from vehicles.models import Vehicle
from datetime import timedelta
from django.utils import timezone

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
            # Modo edição: desabilita o campo 'vehicle'
            self.fields['vehicle'].disabled = True
        else:
            # Modo criação: exibe apenas veículos disponíveis
            self.fields['vehicle'].queryset = Vehicle.objects.filter(status='available')

        if show_status:
            self.fields['status'] = forms.ChoiceField(
                choices=STATUS_CHOICES,
                widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
                label='Status'
            )
            # Se quiser que o campo status apareça como desabilitado, atribua o valor atual
            if self.instance and self.instance.pk:
                self.fields['status'].initial = self.instance.status

    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        expected_end_date = cleaned_data.get('expected_end_date')
        start_date = self.instance.start_date or timezone.now()

        if vehicle and vehicle.status != 'available' and not self.instance.pk:
            raise forms.ValidationError("Veículo não está disponível para manutenção.")

        if expected_end_date:
            max_date = (start_date + timedelta(days=30)).date()
            if expected_end_date > max_date:
                self.add_error(
                    'expected_end_date',
                    "A previsão de conclusão não pode ser maior que 30 dias após o início da manutenção."
                )

        return cleaned_data
