"""
API V1: Walnut URLs
"""

###
# Libraries
###

from django.conf.urls import url, include
from rest_framework_nested import routers

from walnut.api.v1 import views

###
# Router
###
router = routers.SimpleRouter()
router.register(r'walnut', views.VideoViewSet, basename='walnut')


###
# URLs
###
urlpatterns = [
    url(r'^', include(router.urls)),
]