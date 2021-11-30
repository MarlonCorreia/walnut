"""
Walnut S3 helper
"""

###
#  Libraries 
###

import os
import boto3

###
# S3 helper
###

class S3Helper():
    def __init__(self, aws_key, aws_secret_key, region,):
        session = boto3.Session(
                    aws_access_key_id=aws_key,
                    aws_secret_access_key=aws_secret_key,
                ) 
        self.s3 = session.resource('s3', region_name=region)


    def updaload_files_to_bucket(self, dirs, video_uuid, bucket):     
        for dir in dirs:
            for root, _ , files in os.walk(dir):
                for file in files:
                    s3_dir = f'{video_uuid}/dash/{file}' if 'dash' in root else f'{video_uuid}/hls/{file}'
                    self.s3.meta.client.upload_file(f'{root}{file}', bucket, s3_dir)
    