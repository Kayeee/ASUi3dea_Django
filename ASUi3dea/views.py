from django.shortcuts import render, get_object_or_404, render_to_response
from django.core import serializers
from django.contrib.auth.decorators import login_required

from celery import Celery
from .models import Inverter


#app = Celery('tasks', backend='amqp',
                      #broker='amqp://Prafulla:praf1249@10.143.219.16/py_env')

# Create your views here.
def index(request):
    inverter_list_json = serializers.serialize("json", Inverter.objects.all())
    context = {'inverter_list_json': inverter_list_json}
    return render(request, 'ASUi3dea/index.html', context)

@login_required
def loggedin(request):
    inverter_list_json = serializers.serialize("json", Inverter.objects.all())
    context = {'inverter_list_json': inverter_list_json,
                'full_name': request.user.username}
    return render(request,'ASUi3dea/authUser.html', context)
