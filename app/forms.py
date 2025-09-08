# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RefundRequestForm(forms.Form):
    reason = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50, 'placeholder': "Escribí el motivo de tu solicitud"}),
        required=True
    )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")