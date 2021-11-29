"""
Walnut URLs
"""

###
# Libraries
###

from django.conf.urls import url, include


###
# URL Patterns
###
urlpatterns = [
    url(r'^api/v1/', include('walnut.api.v1.urls'))
]