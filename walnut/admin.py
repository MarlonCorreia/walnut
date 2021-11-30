"""
Walnut Admin
"""

###
# Libraries
###

from django.contrib import admin
from walnut.models import Video

###
# Models
###

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ['status', 'dash_file', 'hls_file', 'duration', 
                       'use_hls', 'use_dash']
    list_display = ['id', 'title', 'user', 'status', 'use_hls', 'use_dash']