from django import forms
from .models import Comentario

class EmailPostFormulario(forms.Form):
    nombre = forms.CharField(max_length=25)
    email = forms.EmailField()
    para = forms.EmailField()
    comentarios = forms.CharField(required=False,
                                  widget=forms.Textarea)

class ComentarioFormulario(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('nombre','email','cuerpo')