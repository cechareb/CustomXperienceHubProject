from django import forms

class LoginFormulario(forms.Form):
    usuario = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)