from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^industries/$', views.IndustryList.as_view()),
    url(r'^apps/register', views.UserList.as_view()),
    url(r'^industries/(?P<pk>[0-9]+)/$', views.IndustryDetail.as_view()),
    url(r'^industries/upload', views.IndustryUpload.as_view()),
    url(r'^industries/delete', views.IndustryDelete.as_view()),

]
