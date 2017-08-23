from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'exchange'
urlpatterns = [
    url(r'^$', views.dashboard.as_view(), name='dashboard'),
    url(r'^send$', login_required(views.send.as_view()), name='send'),
    url(r'^request$', views.request.as_view(), name='request'),
    url(r'^account$', views.update_profile, name='account'),
    url(r'^history$', views.history, name='history'),
    url(r'^historicaldata', views.historicaldata, name='historicaldata'),
    url(r'^createcontact$', views.createcontact, name='createcontact'),
    url(r'^contacts$', views.contacts, name='contacts'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^checkwallet$', views.checkwallet, name='checkwallet'),
    url(r'^processing$', views.processing, name='processing'),
]

