from django.conf.urls import url
from . import views

app_name = 'RSR'

urlpatterns = [

    # /RSR/
    url(r'^$', views.search, name='search'),
]