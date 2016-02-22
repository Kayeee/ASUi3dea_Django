from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json
from django.core.serializers.json import DjangoJSONEncoder

from .models import Inverter

@login_required
def save_controls(request):
    if request.method == "POST" and request.is_ajax:
        #This can probalby be done better but I can't figure it out
        #The POST request sends Either "True" or nothing for the checkbox
        try:
            invt_to_chng = Inverter.objects.get(pk=request.POST['pk'])

            try:
                invt_to_chng.state = request.POST['on_off']
            except:
                invt_to_chng.state = False

            invt_to_chng.save()
            msg = "Data Saved"

        except:
            msg = "Please select a point"

    else:
        msg = "GET petitions are not allowed for this view."

    return HttpResponse(msg)

def get_inverter_data(request):
    lat = request.GET['lat']
    lng = request.GET['lng']

    selectedInverter = Inverter.objects.filter(latitude=lat, longitude = lng)
    if (lng or lat) is None:
        return HttpResponseBadRequest("No Inverters found")
    data = serializers.serialize("json", selectedInverter)
    return HttpResponse(data)
