from django import forms
from .models import CustomUser, UploadedFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'birth_year', 'address', 'public_visibility')  


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '**********'
        })
    )

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file', 'title', 'description', 'visibility', 'cost', 'year_published']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': 'application/pdf,image/jpeg'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'visibility': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'year_published': forms.NumberInput(attrs={'class': 'form-control'}),
        }    
    

                