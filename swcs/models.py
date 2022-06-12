from email.policy import default
from statistics import mode
from django.db import models
from django.conf import settings


class sheet_property(models.Model):
    property_name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=4000, null=True)
    function_id = models.IntegerField()


class character_manager(models.Manager):
    def user_characters(self, user, *args, **kwargs):
        return super().get_queryset().filter(player=user)


class character(models.Model):
    character_name = models.CharField(max_length=128)
    character_description = models.CharField(max_length=4000, null=True)
    player = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    character_image = models.ImageField(upload_to='swcs/character_pics/', null=True)
    character_props = models.ManyToManyField(sheet_property, through='character_properties')

    objects = character_manager()


class character_properties(models.Model):
    character = models.ForeignKey(character, on_delete=models.CASCADE)
    prop = models.ForeignKey(sheet_property, on_delete=models.CASCADE)
