"""itp_clc URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.views import login
import django.contrib.auth.views as auth_views 
from django.contrib.auth.views import logout
from django.conf.urls import patterns
from EB import views
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.home),
#   url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^login/$', auth_views.login, name='auth_views.login'),
    url(r'^logout/$', views.logout_page),
    url(r'^register/$', views.register),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^sitemap.txt$', views.sitemap),
    url(r'^contribute/$', views.contribute, name='contribute'),
    url(r'^thanks/$',views.thanks,name='thanks'),
    url(r'^register/success/$', views.success),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^survivors-registry$',views.survivors),
    url(r'^survivors-registry/eldorado-broughams/active$',include('EB.urls')),
    url(r'^survivors-registry/eldorado-broughams/',include('EB.urls')),
    url(r'^survivors-registry/professional-cars/',views.survivors),
    url(r'^survivors-registry/1974-1976-fleetwood-talisman/',views.survivors),
    url(r'^historical-information$',views.historical),
    url(r'^historical-information/eldorado-brougham/active$',views.ebparts, name = 'ebparts'),
    url(r'^historical-information/eldorado-brougham/part-2/(?P<sectionorder>[0-9]+)$',views.historicaltemplate, name ='historicaltemplate'),
    url(r'^historical-information/eldorado-brougham/$',views.ebparts, name = 'ebparts'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
