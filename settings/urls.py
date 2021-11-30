"""
settings URL Configuration
"""

###
# Libraries
###

from django.contrib import admin

from django.conf.urls import url, include

from helpers.health_check import health_check

admin.autodiscover()

urlpatterns = [
    url(f'^admin/', admin.site.urls),
    url(r'^', include('accounts.urls')),
    url(r'^', include('walnut.urls')),

    #Health Check
    url(r'health-check/$', health_check, name='health_check'),
]
