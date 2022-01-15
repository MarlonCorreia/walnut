"""
API V1: Walnut Views
"""

###
# Libraries
###

from rest_framework import permissions, mixins, viewsets
from rest_framework import pagination
from rest_framework.decorators import action
from rest_framework.response import Response

from walnut.models import Video
from walnut.api.v1 import serializers
from walnut.tasks import process_video

###
# Views
###

class VideoViewSet(viewsets.GenericViewSet, 
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin
        ):

        queryset = Video.objects.all().select_related('user')
        serializer_class = serializers.VideoSerializer
        permission_classes = (permissions.IsAuthenticated, )
        pagination_class = pagination.LimitOffsetPagination

        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            content = serializer.save(user=request.user, status='Running')

            process_video.delay(video_id=content.id, 
                                video_uuid=content.uuid,
                                video_source=content.video_source, 
                                use_hls=content.use_hls,
                                use_dash=content.use_dash,
                                aws_credentials=serializer.validated_data.get('aws_credentials'))
            
            return Response(data=serializer.data, status=204)



