
"""
Walnuts FFMPeg wrapper service
"""
import os
from urllib.request import urlretrieve

import ffmpeg_streaming as ffmpeg
from ffmpeg_streaming import Formats, FFProbe

from helpers.utils import create_dir


class FFMPeg():
    """
    Wrappeer for FFMpeg lib
    """

    def __init__(self, video_uuid, 
                       video_url,
                       video_dir, 
                       use_hls, 
                       use_dash):
                       
        self.video_url = video_url
        self.video_uuid = video_uuid
        self.video_dir = video_dir
        self.dash = None
        self.hls = None
        
        self.video_path = self._download_video()

        self.video = ffmpeg.input(self.video_path)
        self.meta_data = FFProbe(self.video_path) 
        

        if use_dash:
            self.dash =  self._generate_dash()
        if use_hls:
            self.hls = self._generate_hls()

    def _generate_hls(self):
        hls = self.video.hls(Formats.h264())
        hls.auto_generate_representations()
        hls.output(f'{self.video_dir}hls/{self.video_uuid}.m3u8')

        return hls

    def _generate_dash(self):
        dash = self.video.dash(Formats.h264())
        dash.auto_generate_representations()
        dash.output(f'{self.video_dir}dash/{self.video_uuid}.mpd')

        return dash

    def _get_video_duration(self):
        return self.meta_data.format().get("duration", 0)        

    def _download_video(self):
        create_dir(self.video_dir, multiple=True)
        create_dir(f'{self.video_dir}/dash')
        create_dir(f'{self.video_dir}/hls')
        
        try:
            data = urlretrieve(self.video_url, f'{self.video_dir}/{self.video_uuid}.mp4')
        except:
            pass

        return data[0]