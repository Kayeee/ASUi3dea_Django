from django.conf.urls import url

from . import views, accountViews, queries

app_name = 'ASUi3dea'
urlpatterns = [
    # ex: /ASUi3dea/
    url(r'^$', accountViews.login, name='login'),
    #Login
    url(r'^login/$', accountViews.login, name='login' ),
    url(r'^save_controls/$', queries.save_controls, name='save_controls' ),
    url(r'^rabbitTest/$', queries.rabbitTest, name='rabbitTest' ),
    url(r'^get_pi_data/$', queries.get_pi_data, name='get_pi_data' ),
    url(r'^auth/$', accountViews.auth_view, name='auth_view' ),
    url(r'^logout/$', accountViews.logout, name='logout' ),
    url(r'^authUser/$', views.loggedin, name='loggedin' ),
    url(r'^basicUser/$', views.loggedin_basic, name='loggedin_basic'),
    url(r'^invalid/$', accountViews.invalid_login, name='invalid_login' ),
    url(r'^(?P<inverter_pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<inverter_pk>[0-9]+)/(?P<data_set>.*)/$', queries.get_inverter_data, name='get_inverter_data')
]
