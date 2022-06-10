from django.db import models
from django.conf import settings


class character(models.Model):
    character_name = models.CharField(max_length=64)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               on_delete=models.CASCADE) 