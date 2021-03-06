"""
Walnut tasks
"""

###
# Libraries
###

import logging
from celery import shared_task

from walnut.models import Video
from walnut.ffmpeg import FFMPeg
from helpers.s3 import S3Helper
from helpers.utils import delete_dir
from settings.settings import BASE_DIR

logger = logging.getLogger('amazon-logs')

###
# Tasks
###

@shared_task
def process_video(video_id, aws_credentials):
    logger.info(f'Start video processing video id {video_id}')
    
    try:
        s3_manager = S3Helper(aws_credentials.get('access_key'), aws_credentials.get('secret_key'), aws_credentials.get('region'))
        bucket = aws_credentials.get('bucket')
    except Exception as ex:
        raise ex
    try:
        video = Video.objects.get(id=video_id)
        video_dir = f'{BASE_DIR}/tmp/{video.uuid}/'
        
        try:
            ffm = FFMPeg(video.uuid, video.video_source, video_dir, video.use_hls, video.use_dash)
        except Exception as e:
            raise e

        dirs = []
        if video.use_hls:
            video.hls_file = f'https://{bucket}.s3.amazonaws.com/{video.uuid}/hls/{video.uuid}.m3u8' 
            dirs.append(f'{video_dir}hls/')
        if video.use_dash:
            video.dash_file = f'https://{bucket}.s3.amazonaws.com/{video.uuid}/dash/{video.uuid}.mpd'
            dirs.append(f'{video_dir}dash/')

        try:
            s3_manager.updaload_files_to_bucket(dirs, video.uuid, aws_credentials.get('bucket'))    
        except Exception as e:
            raise e

        video.duration = ffm._get_video_duration()
        video.status = 'Success'
        video.save()

        delete_dir(video_dir)
        
    except Video.DoesNotExist:
        logger.error(f'Video object does not exist')