"""
settings URL Configuration
"""

from django.contrib import admin

from django.conf.urls import url, include

admin.autodiscover()

urlpatterns = [
    url(f'^admin/', admin.site.urls),
    url(r'^', include('accounts.urls')),
    url(r'^', include('walnut.urls'))
]
