from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views, accountViews, queries

app_name = 'ASUi3dea'
urlpatterns = [

    #accountViews.py
    url(r'^$', RedirectView.as_view(url='login', permanent=False), name='login'),
    url(r'^login/$', accountViews.login, name='login' ),
    url(r'^logout/$', accountViews.logout, name='logout' ),
    url(r'^invalid/$', accountViews.invalid_login, name='invalid_login' ),
    url(r'^auth/$', accountViews.auth_view, name='auth_view' ),

    #views.py
    url(r'^authUser/$', views.loggedin, name='loggedin' ),
    url(r'^authUser/choropleth/(?P<data_type>.*)/$', views.choropleth_data, name='choropleth_data' ),
    url(r'^basicUser/$', views.loggedin_basic, name='loggedin_basic'),
    url(r'^(?P<inverter_pk>[a-z0-9]+-[0-9]+)/$', views.detail, name='detail'),

    #queries.py
    url(r'^save_controls/$', queries.save_controls, name='save_controls' ),
    url(r'^save_data/$', queries.save_data, name='save_data' ),
    url(r'^rabbitTest/$', queries.rabbitTest, name='rabbitTest' ),
    url(r'^get_pi_data/$', queries.get_pi_data, name='get_pi_data' ),
    url(r'^register_pi/$', queries.register_pi, name='register_pi' ),
    url(r'^register_inverter/$', queries.register_inverter, name='register_inverter' ),
    url(r'^update/$', queries.recieve_data_to_save, name='recieve_data_to_save'),
    url(r'^create_group/$', queries.create_group, name='create_group'),
    url(r'^add_to_group/$', queries.add_to_group, name='add_to_group'),
    url(r'^(?P<inverter_pk>[a-z0-9]+-[0-9]+)/single_overview/$', queries.single_overview, name='single_overview' ),
    url(r'^(?P<inverter_pk>[a-z0-9]+-[0-9]+)/update/$', queries.pull_data_from_inverter, name='pull_data_from_inverter'),
    url(r'^(?P<inverter_pk>[a-z0-9]+-[0-9]+)/(?P<data_set>.*)/$', queries.get_inverter_data, name='get_inverter_data')
]
