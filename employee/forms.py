from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'cpf', 'email', 'phone',
                  'address', 'position', 'active']
        labels = {
            'position': 'Cargo'
        }
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
            'position': forms.Select(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            raise forms.ValidationError("CPF inválido. Deve conter 11 dígitos.")
        if Employee.objects.exclude(id=self.instance.id).filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = ''.join(filter(str.isdigit, phone))
        if len(phone) != 11:
            raise forms.ValidationError("Telefone deve conter 11 dígitos, incluindo DDD.")
        return phone
