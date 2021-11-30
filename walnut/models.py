f"""
Walnut Models
"""

###
# Libraries
###
import uuid

from django.db import models
from django.utils.translation import ugettext as _


###
# Models
###

class VideoManager(models.Manager):

    def create(self, **data):
        if data.get('aws_credentials'):
            del data['aws_credentials']

        return super().create(**data)

class Video(models.Model):

    class StatusChoices(models.TextChoices):
            SUCCESS = 'Success', _('Success')
            FAILED = 'Failed', _('Failed')
            RUNNING = 'Running', _('Running')

    uuid = models.UUIDField(
        verbose_name=_('UUID'),
        default=uuid.uuid4,
        editable=False

    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=300,
        blank=True,
        null=True
    )

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True
    )

    video_source = models.URLField(
        verbose_name=_("Video "),
        max_length=200
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.RUNNING
    )

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    webhook_url = models.URLField(
        verbose_name=_("Webhook URL"),
        max_length=200, 
        null=False,
        blank=False
    )

    use_dash = models.BooleanField(
        verbose_name=_("Use Dash"),
        default=False,
        null=False
    )

    dash_file = models.URLField(
        verbose_name=_("Dash file"),
        max_length=200,
        null=True,
        blank=True,
        help_text="This field will be auto generated"
    )

    use_hls = models.BooleanField(
        verbose_name=_("Use HLS"),
        default=False,
        null=False
    )

    hls_file = models.URLField(
        verbose_name=_("HLS file"),
        max_length=200,
        null=True,
        blank=True,
        help_text="This field will be auto generated"
    )

    
    duration = models.FloatField(
        verbose_name=_("Duration"),
        default=0,
        help_text="This field will be auto generated"
    )

    objects = VideoManager()
    
    