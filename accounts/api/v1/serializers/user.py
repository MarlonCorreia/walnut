"""
API V1: Accounts Serializers
"""
###
# Libraries
###
from rest_auth.serializers import (
    UserDetailsSerializer as BaseUserDetailsSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


###
# Serializers
###
class UserDetailsSerializer(BaseUserDetailsSerializer):

    class Meta(BaseUserDetailsSerializer.Meta):
        model = User
        fields = (
            'id',
            'username',
            'email',
            'name',
        )