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
from django.contrib import admin
from django.urls import path

from msdn import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('browse', views.browse_groups, name='browse'),
    path('search', views.search_result, name='search_result'),
    path('groups/<int:group_id>', views.group_detail, name='group_detail'),
    path('families/', views.family_list, name='family_list'),
    path('families/<int:family_id>', views.family_detail, name='family_detail'),
    path('files/<int:file_id>', views.file_detail, name='file_detail'),
    path('admin/', admin.site.urls),
]
