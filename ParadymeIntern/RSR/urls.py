from django.conf.urls import url
from . import views

app_name = 'RSR'

urlpatterns = [

    #/index
    url(r'^$', views.person_list, name='person_list'),
]