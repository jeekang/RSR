"""ParadymeIntern URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from. import views
from RSR.views import *

app_name = 'RSR'


urlpatterns = [

    url(r'^uploaddoc/$', uploaddoc, name='uploaddoc'),
    url(r'^uploadlist/$', uploadlist, name = 'uploadlist'),
    url(r'^listdelete/$', listdelete, name="listdelete"),
    url(r'^main/$', main, name = 'main'),
    url(r'^search/$', search, name='search'),

    #Edit page
    url(r'^edit/(?P<person_id>\d+)/$', views.person_edit, name='person-edit'),
    url(r'^edit_skill/(?P<skill_id>\d+)/$', views.skill_edit, name='skill-edit'),

    url(r'^logout/$', views.logout_page, name = 'logout'),

    #Search/Export Team
    url(r'^search/person_detail/(?P<pk>[0-9]+)/$', views.detail, name='detail'),


]

