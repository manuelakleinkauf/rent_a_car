from django import forms
from django.core.exceptions import ValidationError
from reservation.models import Reservation
from .models import Client
from vehicles.models import Vehicle

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'cpf', 'email', 'phone', 'address', 'active']
        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 2,               
                'style': 'resize:none;',
                'class': 'form-control', 
            }),
          
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = ''.join(filter(str.isdigit, cpf))  
        if len(cpf) != 11:
            raise forms.ValidationError("CPF inválido. Deve conter 11 dígitos.")
        if Client.objects.exclude(id=self.instance.id).filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = ''.join(filter(str.isdigit, phone)) 
        if len(phone) != 11:
            raise forms.ValidationError("Telefone deve conter 11 dígitos, incluindo DDD.")
        return phone
    
    def clean(self):
        cleaned_data = super().clean()
        active = cleaned_data.get('active')

        # Só faz a validação se o cliente estiver tentando ficar inativo
        if active is False and self.instance.pk:
            # Verifica se o cliente tem reservas ativas
            has_active_reservations = Reservation.objects.filter(client=self.instance).exists()
            # Ou se o cliente tem algum veículo alugado (ajuste conforme seu modelo)
            has_rented_vehicles = Vehicle.objects.filter(
                reservation__client=self.instance,
                status='rented'
            ).exists()
            if has_active_reservations or has_rented_vehicles:
                raise ValidationError("Cliente não pode ser inativado pois possui reservas ou veículos alugados.")

        return cleaned_data



