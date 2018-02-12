from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^industries/$', views.IndustryList.as_view()),
]
