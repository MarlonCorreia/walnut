"""
API V1: Accounts Serializers
"""

###
# Libraries
###
from django.contrib.auth import get_user_model

from rest_auth.models import TokenModel
from rest_framework import serializers
from rest_auth.registration.serializers import (
    RegisterSerializer as DefaultRegisterSerializer,
)

from accounts.api.v1.serializers import UserDetailsSerializer


User = get_user_model()


###
# Serializers
###
class UserTokenSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()

    class Meta:
        model = TokenModel
        fields = ('key', 'user',)

class RegisterSerializer(DefaultRegisterSerializer):
    name = serializers.CharField(max_length=300, required=True)


    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['name'] = self.validated_data.get('name', '')

        return data

    def custom_signup(self, request, user):
        user.name = self.cleaned_data.get('name')
        user.save()