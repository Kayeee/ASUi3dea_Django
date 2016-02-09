from django.conf.urls import url

from . import views

app_name = 'ASUi3dea'
urlpatterns = [
    # ex: /ASUi3dea/
    url(r'^$', views.index, name='index'),
    # ex: /ASUi3dea/5/
    url(r'^(?P<inverter_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /ASUi3dea/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /ASUi3dea/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
