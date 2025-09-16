
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Rating

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

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['title', 'text', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un título corto'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu reseña...'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control d-none',  
                'min': 1,
                'max': 5
            }),
        }