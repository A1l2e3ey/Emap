"""Emap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from Emapapp.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', logout),
    url(r'^friends([0-9]+)/$', friends),
    url(r'^form/$', form),
    url(r'^messageonline/$', messageonline, name='messageonline'),
    url(r'^login/$', login),
    url(r'^favourite([0-9]+)/$', favourite, name='favourite'),
    #url(r'^registration2/$', registration2),
    url(r'^profile([0-9]+)/$', profile),
    url(r'^come([0-9]+=[0-9]{3})/$', come),
    url(r'^notcome([0-9]+=[0-9]{3})/$', notcome),
    url(r'^add([0-9]+)/$', add),
    url(r'^notadd([0-9]+)/$', notadd),
    url(r'^agree([0-9]+=[0-9]{3})/$', agree),
    url(r'^notagree([0-9]+=[0-9]{3})/$', notagree),
    url(r'^change/$', change),
    url(r'^userssearch/$', users),
    url(r'^mybuh([0-9]+)/$', mybuh),
    url(r'^addfriend([0-9]+)/$', addfriend),
    url(r'^yetbuh([0-9]+)/$', yetbuh),
    url(r'^ktoidet([0-9]{3})/$', ktoidet),
    url(r'^podpis([0-9]{3})/$', podpis),
    url(r'^otpis([0-9]{3})/$', otpis),
    # url(r'^registration/$', registration),
    url(r'^mes([0-9]+)/$', messages),
    url(r'^calendar/$', calendar),
    url(r'^$', index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
