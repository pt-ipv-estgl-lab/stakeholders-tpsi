from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']  # Exclude the 'user' field from the form

    old_password = forms.CharField(label='Old password *', widget=forms.PasswordInput)
    new_password = forms.CharField(label='Nova password *', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmar Password *', widget=forms.PasswordInput)
