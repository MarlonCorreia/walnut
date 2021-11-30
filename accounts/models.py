"""
Accounts Models
"""

###
# Libs
###
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _

###
# Accounts Models
###

class User(AbstractUser):

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=300,
        blank=True
    )
