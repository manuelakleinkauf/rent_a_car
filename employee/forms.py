from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'cpf', 'email', 'phone',
                  'address', 'active', 'position']
        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 2,               # altura menor
                'style': 'resize:none;',  # não deixa redimensionar
                'class': 'form-control',  # para estilo Bootstrap (se usar)
            }),
            # Opcional: já define classes Bootstrap para outros campos
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        # Remove qualquer caractere não numérico
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            raise forms.ValidationError(
                "CPF inválido. Deve conter 11 dígitos.")
        if Employee.objects.exclude(id=self.instance.id).filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Remove qualquer caractere não numérico
        phone = ''.join(filter(str.isdigit, phone))
        if len(phone) != 11:
            raise forms.ValidationError(
                "Telefone deve conter 11 dígitos, incluindo DDD.")
        return phone
