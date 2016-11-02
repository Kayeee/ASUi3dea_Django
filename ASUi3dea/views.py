from django.shortcuts import render, get_object_or_404, render_to_response
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.apps import apps
import json
from celery import Celery
from .models import *

@login_required
def loggedin(request):
    groups = request.user.userprofile.invertergroup_set.all()
    groups_json = []
    counter = 0

    #construct json
    for group in groups:
        groups_json.append({})
        groups_json[counter]["name"] = group.name
        groups_json[counter]["inverters"] = []
        counter2 = 0

        for inverter in group.inverter_set.all():
            groups_json[counter]["inverters"].append({})
            groups_json[counter]["inverters"][counter2]["inverterName"] = inverter.id
            groups_json[counter]["inverters"][counter2]["lat"] = inverter.pi.latitude
            groups_json[counter]["inverters"][counter2]["lon"] = inverter.pi.longitude
            counter2 += 1

        counter += 1
    print groups_json
    groups_json = json.dumps(groups_json)
    #groups_json = serializers.serialize("json", groups)
    pi_list_json = serializers.serialize("json", Pi.objects.all())
    models = apps.get_app_config('ASUi3dea').get_models()
    wanted_models = []
    for model in models:
        if (model.__name__ is not 'Pi') and (model.__name__ is not 'Inverter'):
            wanted_models.append(model.__name__)
    wanted_models = json.dumps(wanted_models)
    context = {'pi_list_json': pi_list_json,
                'groups_json': groups_json,
                'full_name': request.user.username,
                'available_models': wanted_models}
    return render(request,'ASUi3dea/authUser.html', context)

@login_required
def choropleth_data(request, data_type):
    #TODO: ELIMATE THIS NEXT SECTION. IT IS A COPY OF STUFF DONE IN 'loggedin'
    pi_list_json = serializers.serialize("json", Pi.objects.all())
    models = apps.get_app_config('ASUi3dea').get_models()
    wanted_models = []
    for model in models:
        if (model.__name__ is not 'Pi') and (model.__name__ is not 'Inverter'):
            wanted_models.append(model.__name__)
    wanted_models = json.dumps(wanted_models)
    context = {'pi_list_json': pi_list_json,
                'full_name': request.user.username,
                'available_models': wanted_models}
    #END OF TO DO SECTION. I SHOULDN'T HAVE HAD TO WRITE THAT CODE TWICE SHOULD BE EASILY FIXABLE LATER.
    model = apps.get_model(app_label='ASUi3dea', model_name=data_type)
    states = Address.objects.values('state').distinct()
    stateValues = {}
    for state in states:
        ads_for_pis = Address.objects.filter(state = state['state'])
        inverters = []
        for a in ads_for_pis:

            inverters = [x for x in a.pi.inverter_set.all()]
        all_datas = [i.temperature_set.last() for i in inverters]
        total = 0.0
        for data in all_datas:
            if data is not None:
                total += data.get_data()[1]
        stateValues[state['state']] = total/len(all_datas)
        print(stateValues)
        context['stateValues'] = json.dumps(stateValues)

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

@login_required
def registerDevice(request):
    return render(request, 'ASUi3dea/registerDevice.html')
