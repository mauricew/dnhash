"""msdnhash URL Configuration

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

from msdn import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about', views.about, name='about'),
    url(r'^browse', views.browse_groups, name='browse'),
    url(r'^groups/(?P<group_id>[0-9]+)$', views.group_detail, name='group_detail'),
    url(r'^families/(?P<family_id>[0-9]+)$', views.family_detail, name='family_detail'),
    url(r'^files/(?P<file_id>[0-9]+)$', views.file_detail, name='file_detail'),
    url(r'^admin/', admin.site.urls),
]
