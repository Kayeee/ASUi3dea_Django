from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Question, Inverter

# Create your views here.
def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    inverter_list = Inverter.objects.all()
    context = {'inverter_list': inverter_list}
    return render(request, 'ASUi3dea/index.html', context)

def detail(request, inverter_id):
    inverter = get_object_or_404(Inverter, pk=inverter_id)
    return render(request, 'ASUi3dea/detail.html', {'inverter': inverter})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
