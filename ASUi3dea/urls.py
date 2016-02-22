from django.conf.urls import url

from . import views, accountViews, queries

app_name = 'ASUi3dea'
urlpatterns = [
    # ex: /ASUi3dea/
    url(r'^$', views.index, name='index'),
    #Login
    url(r'^login/$', accountViews.login, name='login' ),
    url(r'^save_controls/$', queries.save_controls, name='save_controls' ),
    url(r'^get_inverter_data/$', queries.get_inverter_data, name='get_inverter_data' ),
    url(r'^auth/$', accountViews.auth_view, name='auth_view' ),
    url(r'^logout/$', accountViews.logout, name='logout' ),
    url(r'^authUser/$', views.loggedin, name='loggedin' ),
    url(r'^invalid/$', accountViews.invalid_login, name='invalid_login' ),
]
