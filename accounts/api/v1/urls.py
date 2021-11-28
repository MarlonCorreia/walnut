"""
API V1: Accounts Urls
"""
###
# Libraries
###
from django.conf.urls import url
from rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordChangeView,
    PasswordResetView,
)
from rest_auth.registration.views import (
    RegisterView,
)

###
# URLs
###

urlpatterns = [
    url(
        r'^login/$',
        LoginView.as_view(),
        name='rest_login',
    ),
    url(
        r'^logout/$',
        LogoutView.as_view(),
        name='rest_logout',
    ),
    url(
        r'^user/$',
        UserDetailsView.as_view(),
        name='rest_user_details',
    ),
    url(
        r'^change-password/$',
        PasswordChangeView.as_view(),
        name='rest_password_change',
    ),
    url(
        r'^password/reset/$',
        PasswordResetView.as_view(),
        name='rest_password_reset',
    ),
    url(
        r'^register/$',
        RegisterView.as_view(),
        name='rest_register',
    ),
]