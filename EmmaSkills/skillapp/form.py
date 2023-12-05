from django import forms

class PasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

class ConfirmReset(forms.Form):
    password = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'Password'})
    Conf_password = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'Password'})