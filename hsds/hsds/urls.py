"""hsds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin, auth
from django.http import request

from event.views import events_view, home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^events/', include('event.urls')),
    url(r'^admission/', include('admission.urls')),
    url(r'^accounts/', include('login.urls')),
    url(r'^events/$', events_view, name="events"),
    url(r'^$', home, name="home"),
]
