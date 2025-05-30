from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'address','image' , 'password')
        widgets = {
            'password': forms.PasswordInput()
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'address','image' , 'password')
        widgets = {
            'password': forms.PasswordInput()
        }