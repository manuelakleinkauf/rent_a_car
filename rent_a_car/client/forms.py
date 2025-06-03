from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'cpf', 'email', 'phone', 'address', 'active']
        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 2,               # altura menor
                'style': 'resize:none;', # não deixa redimensionar
                'class': 'form-control', # para estilo Bootstrap (se usar)
            }),
            # Opcional: já define classes Bootstrap para outros campos
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = ''.join(filter(str.isdigit, cpf))  # Remove qualquer caractere não numérico
        if len(cpf) != 11:
            raise forms.ValidationError("CPF inválido. Deve conter 11 dígitos.")
        if Client.objects.exclude(id=self.instance.id).filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = ''.join(filter(str.isdigit, phone))  # Remove qualquer caractere não numérico
        if len(phone) != 11:
            raise forms.ValidationError("Telefone deve conter 11 dígitos, incluindo DDD.")
        return phone



