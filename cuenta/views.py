from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .forms import LoginFormulario

def usuario_login(request):
    if request.method == 'POST':
        formulario = LoginFormulario(request.POST)
        if formulario.is_valid():
            cd = formulario.cleaned_data
            usuario = authenticate(request,
                                   username=cd['usuario'],
                                   password=cd['password'])
            if usuario is not None:
                if usuario.is_active:
                    login(request, usuario)
                    return HttpResponse('Autenticado '\
                                        'satisfactoriamente')
                else:
                    return HttpResponse('Cuenta desactivada')
            else:
                return HttpResponse('Login invalido')
    else:
        formulario = LoginFormulario()

    return render(request, 'cuenta/login.html', {'formulario':formulario})

@login_required
def dashboard(request):
    return render(request,
                  'cuenta/dashboard.html',
                  {'seccion': 'dashboard'})