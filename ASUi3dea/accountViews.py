from django.core.context_processors import csrf
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, Http404, HttpResponseRedirect

from .models import Inverter

def login(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'ASUi3dea/login.html', c)

def invalid_login(request):
    return render(request, 'ASUi3dea/invalid_login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'ASUi3dea/logout.html')

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/ASUi3dea/authUser')
    else:
        return HttpResponseRedirect('/ASUi3dea/invalid')
