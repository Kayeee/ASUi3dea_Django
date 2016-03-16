from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json
from django.core.serializers.json import DjangoJSONEncoder
import time
from django.db import models

from .models import Inverter, Pi
from celery import Celery
from .tasks import add


def rabbitTest(request):
    result = add.delay(request)
    time.sleep(10)
    return HttpResponse(result.status)

@login_required
def save_controls(request):

    if request.method == "POST" and request.is_ajax:
        #This can probalby be done better but I can't figure it out
        #The POST request sends Either "True" or nothing for the checkbox
        try:
            invt_to_chng = Inverter.objects.get(pk=request.POST['pk'])

            try:
                invt_to_chng.state = request.POST['on_off']
                #result = add.delay(1)
            except:
                invt_to_chng.state = False
                #result = add.delay(0)

            #while not result.status:
            #    time.sleep(0)

            invt_to_chng.save()
            #msg = result.get()
            msg="Data Saved"

        except:
            msg = "Please select a point"

    else:
        msg = "GET petitions are not allowed for this view."

    return HttpResponse(msg)

def get_pi_data(request):
    lat = request.GET['lat']
    lng = request.GET['lng']

    if (lng or lat) is None:
        return HttpResponseBadRequest("No Pi's found")

    selectedPi = Pi.objects.filter(latitude=lat, longitude = lng)
    inverters = selectedPi[0].inverter_set.all()

    data = serializers.serialize("json", inverters)
    return HttpResponse(data)

def get_inverter_data(request, inverter_pk, data_set):
    inverter = Inverter.objects.get(pk=inverter_pk)
    data = getattr(inverter, data_set).all()

    #all we need is the timestamp and data here.
    data_tuples = []
    for piece in data:
        data_tuples.append(piece.get_data())

    #data_tuples = serializers.serialize("json", data_tuples)
    return JsonResponse(data_tuples, safe=False)
