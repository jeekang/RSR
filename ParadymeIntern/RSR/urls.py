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
    url(r'^edit_company/(?P<company_id>\d+)/$', views.company_edit, name='company-edit'),
    url(r'^edit_school/(?P<school_id>\d+)/$', views.school_edit, name='school-edit'),
    url(r'^edit_course/(?P<course_id>\d+)/$', views.course_edit, name='course-edit'),
    url(r'^edit_language/(?P<language_id>\d+)/$', views.language_edit, name='language-edit'),
    url(r'^edit_sidepro/(?P<sidepro_id>\d+)/$', views.sidepro_edit, name='sidepro-edit'),
    url(r'^edit_award/(?P<award_id>\d+)/$', views.award_edit, name='award-edit'),
    url(r'^edit_club/(?P<club_id>\d+)/$', views.club_edit, name='club-edit'),
    url(r'^edit_volunteer/(?P<volunteer_id>\d+)/$', views.volunteer_edit, name='volunteer-edit'),
    url(r'^edit_professional/(?P<pro_id>\d+)/$', views.professional_edit, name='professional-edit'),
    url(r'^edit_clearance/(?P<clearance_id>\d+)/$', views.clearance_edit, name='clearance-edit'),

    #Delete
    url(r'^delete_skill/(?P<pk>\d+)$', views.skill_delete, name="skill-delete"),
    url(r'^delete_company/(?P<pk>\d+)/$', views.company_delete, name="company-delete"),
    url(r'^delete_school/(?P<pk>\d+)/$', views.school_delete, name="school-delete"),
    url(r'^delete_course/(?P<pk>\d+)/$', views.course_delete, name="course-delete"),
    url(r'^delete_language/(?P<pk>\d+)/$', views.language_delete, name='language-delete'),
    url(r'^delete_sidepro/(?P<pk>\d+)/$', views.sidepro_delete, name='sidepro-delete'),
    url(r'^delete_award/(?P<pk>\d+)/$', views.award_delete, name='award-delete'),
    url(r'^delete_club/(?P<pk>\d+)/$', views.club_delete, name='club-delete'),
    url(r'^delete_volunteer/(?P<pk>\d+)/$', views.volunteer_delete, name='volunteer-delete'),
    url(r'^delete_professional/(?P<pk>\d+)/$', views.professional_delete, name='professional-delete'),

    #ocr search
    url(r'^resumesearch',OCRSearch, name='ocrsearch'),


    url(r'^logout/$', views.logout_page, name = 'logout'),
    url(r'^search/person_detail/(?P<pk>[0-9]+)/$', views.detail, name='detail'),

        #url for autocomplete function for ProfessionalDevelopment class
    url(r'^search/ProfessionalDevelopment-autocomplete/$', ProfessionalDevelopmentAutocomplete.as_view(),
        name='ProfessionalDevelopment-autocomplete',),
        #url for autocomplete function for skills class
    url(r'^search/Skills-autocomplete/$', Skillsutocomplete.as_view(),
        name='Skills-autocomplete',),
        #url for autocomplete function for Volunteering class
    url(r'^search/Volunteering-autocomplete/$', Volunteeringautocomplete.as_view(),
        name='Volunteering-autocomplete',),
        #url for autocomplete function for search bar
    url(r'^search/SearchBar-autocomplete/$', SearchBarautocomplete.as_view(),
        name='SearchBar-autocomplete',),
        #url for autocomplete function for LanguageSpoken class
    url(r'^search/Language-autocomplete/$', Languageautocomplete.as_view(),
        name='LanguageSpoken-autocomplete',),
        #url for autocomplete function for Company class
    url(r'^search/Company-autocomplete/$', Companyautocomplete.as_view(),
        name='Company-autocomplete',)


]
