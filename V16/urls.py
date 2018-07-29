"""mysite URL Configuration

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
from django.contrib import admin
from V16 import views
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
    # url(r'^$',views.Home),
    #url(r'(?P<carnum>[0-9]+)$',views.CarPage),
    url(r'^year-(?P<year>[0-9]+)/carupdate/(?P<carnum>[0-9]+)',views.carupdates, name = 'carupdates'),
    url(r'^year-(?P<year>[0-9]+)/',views.cardisplay, name = 'cardisplay'),
    #url(r'^part-2/(?P<sectionorder>[0-9]+)$',views.historicaltemplate, name = 'historicaltemplate'),
    url(r'^$',views.ebparts, name = 'ebparts'),

]
