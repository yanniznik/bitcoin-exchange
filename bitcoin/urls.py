from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('exchange.urls')),
    url(r'^logout/$', views.logout, {'next_page': '/'}, name="logout"),
    url(r'^login/$', views.login, name="login")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)