from django.conf.urls import url

from . import views

app_name = 'exchange'
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^send$', views.send, name='send'),
    url(r'^account$', views.update_profile, name='account'),
    url(r'^history$', views.history, name='history'),
    url(r'^contacts$', views.contacts, name='contacts'),
    url(r'^signup/$', views.signup, name='signup'),
]

