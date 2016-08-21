from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.core import serializers
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import *
from celery import Celery
from .tasks import *


#from .formatter import formatter
import geohash
import re
import time
import json

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

def single_overview(request, inverter_pk ):
    models = apps.get_app_config('ASUi3dea').get_models()
    dataDict = {}
    for model in models:
        if (model.__name__ is not 'Pi') and (model.__name__ is not 'Inverter') and (model.__name__ is not 'Address') and (model.__name__ is not 'UserProfile') and (model.__name__ is not 'InverterGroup'):
            model_object = apps.get_model(app_label='ASUi3dea', model_name=model.__name__)
            print("name: {0}".format(model.__name__))
            instance_list = model_object.objects.filter(inverter_id=inverter_pk)

            if instance_list:
                dataDict[model.__name__] = [(f.get_data()[0],f.get_data()[1]) for f in instance_list]
            # if instance_list:
            #     head.append(model.__name__)
            # if not triplets:

            #     for dataPiece in instance_list:
            #         triplets.append(list(dataPiece.get_data()))
            # else:
            #     counter = 0
            #     for dataPiece in instance_list:
            #         current = instance_list[counter]
            #         triplets[counter].append(dataPiece.get_data()[1])#timestamps are already in there, we just want the values
            #         counter += 1

    print("triplets: {0}".format(dataDict))
    return JsonResponse(dataDict, safe=False)

def power_query(request, inverter_pk):
    data_dict = {}
    input_powers = InputPower.objects.filter(inverter_id=inverter_pk)
    grid_powers = GridPower.objects.filter(inverter_id=inverter_pk)
    if input_powers and grid_powers:
        data_dict[InputPower.__name__] = [(f.get_data()[0],f.get_data()[1]) for f in input_powers]
        data_dict[GridPower.__name__] = [(f.get_data()[0],f.get_data()[1]) for f in grid_powers]
    return JsonResponse(data_dict, safe=False)

def current_query(request, inverter_pk):
    data_dict = {}
    input_currents = InputCurrent.objects.filter(inverter_id=inverter_pk)
    grid_currents = GridCurrent.objects.filter(inverter_id=inverter_pk)
    if input_currents and grid_currents:
        data_dict[InputCurrent.__name__] = [(f.get_data()[0],f.get_data()[1]) for f in input_currents]
        data_dict[GridCurrent.__name__] = [(f.get_data()[0],f.get_data()[1]) for f in grid_currents]
    return JsonResponse(data_dict, safe=False)

def voltage_query(request, inverter_pk):
    data_dict = {}
    input_voltages = InputVoltage.objects.filter(inverter_id=inverter_pk)
    grid_voltages = GridVoltage.objects.filter(inverter_id=inverter_pk)
    if input_voltages and grid_voltages:
        data_dict[InputVoltage.__name__] = [(f.get_data()[0],f.get_data()[1]) for f in input_voltages]
        data_dict[GridVoltage.__name__] = [(f.get_data()[0],f.get_data()[1]) for f in grid_voltages]
    return JsonResponse(data_dict, safe=False)

def efficiency_query(request, inverter_pk):
    data_dict = {}
    efficiencies = ConversionEfficiency.objects.filter(inverter_id=inverter_pk)
    if efficiencies:
        data_dict[ConversionEfficiency.__name__] = [(f.get_data()[0],f.get_data()[1]) for f in efficiencies]
    return JsonResponse(data_dict, safe=False)

def energy_query(request, inverter_pk):
    data_dict = {}
    energies = CumulatedEnergy.objects.filter(inverter_id=inverter_pk)
    if energies:
        data_dict[CumulatedEnergy.__name__] = [(f.get_data()[0],f.day,f.week) for f in energies]
    return JsonResponse(data_dict, safe=False)

def temperature_query(request, inverter_pk):
    data_dict = {}
    temperatures = InverterTemperature.objects.filter(inverter_id=inverter_pk)
    if temperatures:
        data_dict[InverterTemperature.__name__] = [(f.get_data()[0],f.get_data()[1]) for f in temperatures]
    return JsonResponse(data_dict, safe=False)

def get_pi_data(request):
    lat = request.GET['lat']
    lng = request.GET['lng']

    if (lng or lat) is None:
        return HttpResponseBadRequest("No Pi's found")

    selectedPi = Pi.objects.filter(latitude=lat, longitude = lng)
    inverters = selectedPi[0].inverter_set.all()

    data = serializers.serialize("json", inverters)
    return HttpResponse(data)

#gest data from database
def get_inverter_data(request, inverter_pk, data_set):
    inverter = Inverter.objects.get(pk=inverter_pk)
    data = getattr(inverter, data_set).all()

    #all we need is the timestamp and data here.
    data_tuples = []
    for piece in data:
        data_tuples.append(piece.get_data())

    #data_tuples = serializers.serialize("json", data_tuples)
    return JsonResponse(data_tuples, safe=False)

def pull_data_from_inverter(request, inverter_pk):
    pi_id = re.sub(r'-(.*)', '', inverter_pk)
    result_json = getAll.delay(pi_id)
    #result_json = createData()
    while result_json.state != 'SUCCESS':
        print result_json.state
        time.sleep(5)
    #result_json = '{"inverter": "1", "temperature": 25}'
    #print("Result Json: {0}".format(result_json.get()))
    result = json.loads(result_json.get())
    #result = json.loads(result_json)
    print(result)
    save_data(result, pi_id)
    return HttpResponseRedirect('/ASUi3dea/' + inverter_pk)

@csrf_exempt
def recieve_data_to_save(request):
    lat = request.GET.get('lat', -1)
    lon = request.GET.get('lon', -1)
    print("Lat {0} long: {1}".format(float(lat), float(lon)))
    pi_geohash = geohash.encode(float(lat), float(lon), 24)
    print("geohash: {0}".format(pi_geohash))
    inverter = request.GET.get('inverter', -1)
    temperature = request.GET.get('temperature', -1)
    #hs_temp = request.POST.get('HSTemp', -1)
    dc_power = request.GET.get('dcpower', -1)
    ac_power = request.GET.get('acpower', -1)
    status = request.GET.get("status", -1)

    values_dict = {'inverter': inverter, 'temperature': temperature, 'dcpower': dc_power, 'acpower': ac_power, 'status': status}
    #values_dict = {'inverter': inverter, 'temperature': temperature}
    print("Values_dict: {0}".format(values_dict))
    save_data(values_dict, pi_geohash)
    return HttpResponse("Data Recieved Successfully")


def save_data(result, pi_id):
    inverter_id = pi_id + '-' + result["inverter"]
    print("inverter ID: {0}".format(inverter_id))
    for model in result:
        print("Model: {0}".format(model))
        #available_models=apps.get_app_config('ASUi3dea').get_models()
        if model != "inverter":
            #try:
            model_object = apps.get_model(app_label='ASUi3dea', model_name=model)
            new_obj = model_object.objects.create(inverter_id=inverter_id) #create the model object
            if model == "cumulatedenergy":
                new_obj.set_data(result[model]["dailyenergy"], result[model]["weeklyenergy"], result[model]["monthlyenergy"], result[model]["yearlyenergy"], result[model]["totalenergy"])
            else:
                new_obj.set_data(result[model])
            new_obj.save()
            # except:
            #     print("Either Pi or Inverter does not exist")


def register_pi(request):
    lat = request.POST['latitude']
    lon = request.POST['longitude']
    pi_geohash = geohash.encode(lat, lon, 24)

    if not Pi.objects.filter(id=pi_geohash):#No pi's registered
        Pi.objects.create(id=geohash, latitude = lat, longitude=lon)
        return HttpResponse("Successfully registered Pi")
    else:
        return HttpResponse("Pi is already registered")

def register_inverter(request):
    lat = request.POST['latitude']
    lon = request.POST['longitude']
    pi_geohash = geohash.encode(lat, lon, 24)
    if Pi.objects.filter(id=pi_geohash):#Pi is registered
        Inverter.objects.create(pi_id=pi_geohash)
        return HttpResponse("Successfully registered Inverter")
    else:
        return HttpResponse("The Pi you are tyring to register this inverter with does not exist.")

@login_required
def create_group(request):
    user = request.user
    group = request.POST['group']
    inverters = request.POST['inverters']

@login_required
def add_to_group(request):
    user = User.objects.get(username = request.user) #user Object
    group = request.POST['group']
    inverters = request.POST.getlist('inverters[]', False)
    print "user: {0}, group: {1}, inverters: {2}".format(user, group, inverters)
    for i in inverters:
        inverter = Inverter.objects.get(pk = i)
        user.userprofile.invertergroup_set.get(name=group).inverter_set.add(inverter)
    return HttpResponse("Successfully added to group")
