from django import forms
from .models import Maintenance


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['reason', 'expected_end_date']
        widgets = {
            'expected_end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }
