"""
API V1: Walnut Serializers
"""

###
# Libraries
###

from rest_framework import serializers

from walnut.models import Video
from accounts.api.v1.serializers import UserDetailsSerializer


###
# Serializers
###
class VideoSerializer(serializers.ModelSerializer):
    aws_credentials = serializers.JSONField(required=True)
    status = serializers.ReadOnlyField()

    def validate_aws_credentials(self, attrs):
        invalid_attrs = []
        
        if not attrs.get('access_key'):
            invalid_attrs.append('key')
        if not attrs.get('secret_key'):
            invalid_attrs.append('secret_key')
        if not attrs.get('region'):
            invalid_attrs.append('region')
        if not attrs.get('bucket'):
            invalid_attrs.append('bucket')
        
        if invalid_attrs:
            raise serializers.ValidationError(f"Please provide fields {invalid_attrs}")

        return super().validate(attrs)
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "user": UserDetailsSerializer(instance.user).data,
            "description": instance.description,
            "status": instance.status,
            "video_source": instance.video_source,
            "use_hls": instance.use_hls,
            "use_dash": instance.use_dash,
            "webhook_url": instance.webhook_url
        }

    class Meta:
        model = Video
        fields = ['title', 'description', 'video_source', 'status', 'webhook_url', 'use_dash',
                  'use_hls', 'aws_credentials']