# forms.py
from django import forms

class RefundRequestForm(forms.Form):
    reason = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50, 'placeholder': "Escribí el motivo de tu solicitud"}),
        required=True
    )