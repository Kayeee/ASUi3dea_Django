from django.shortcuts import render, get_object_or_404, render_to_response
from django.core import serializers
from django.contrib.auth.decorators import login_required

from celery import Celery
from .models import Inverter, Pi

# Create your views here.

@login_required
def loggedin(request):
    pi_list_json = serializers.serialize("json", Pi.objects.all())
    context = {'pi_list_json': pi_list_json,
                'full_name': request.user.username}
    return render(request,'ASUi3dea/authUser.html', context)

@login_required
def loggedin_basic(request):
    pi_list_json = serializers.serialize("json", Pi.objects.all())
    context = {'pi_list_json': pi_list_json,
                'full_name': request.user.username}
    return render(request,'ASUi3dea/basicUser.html', context)

@login_required
def detail(request, inverter_pk):
    try:
        inverter = Inverter.objects.get(pk=inverter_pk)
        links = [f for f in inverter._meta.get_fields() if (f.one_to_many or f.one_to_one) and f.auto_created]
        links = [rel.get_accessor_name() for rel in links]
        attributes = []
        for link in links:
            #link is 'temperature_set'. getattr.... is the value of the last known temperature
            attribute = (link, getattr(inverter, link).last())
            if getattr(inverter, link).last() is not None:
                #attributes is a tuple containing the '..._set' phrase along with the most recent value of that set.
                attributes.append(attribute)
    except Inverter.DoesNotExist:
        raise Http404("Inverter does not exist")
    return render(request, 'ASUi3dea/detail.html', {'inverter': inverter, 'attributes': attributes})
