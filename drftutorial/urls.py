from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('catalog.urls')),
    url(r'^', include('industry.urls')),
    url(r'^apps/register', obtain_auth_token),
]