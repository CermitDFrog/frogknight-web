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


class species(models.Model):
    species_name = models.CharField(max_length=128)
    species_description = models.TextField(null=True)
    species_brawn = models.IntegerField(default=2)
    species_agility = models.IntegerField(default=2)
    species_intellect = models.IntegerField(default=2)
    species_cunning = models.IntegerField(default=2)
    species_willpower = models.IntegerField(default=2)
    species_presence = models.IntegerField(default=2)
    species_wound = models.IntegerField(null=True)
    species_strain = models.IntegerField(null=True)
    species_starting_xp = models.IntegerField(null=True)
    species_image = models.ImageField(upload_to='swcs/species_pics/', null=True)
    props = models.ManyToManyField(sheet_property, through='species_properties')

    def __str__(self):
        return self.species_name


class species_properties(models.Model):
    species = models.ForeignKey(species, on_delete=models.CASCADE)
    species_property = models.ForeignKey(sheet_property, on_delete=models.CASCADE)


class character(models.Model):
    # Fields
    character_name = models.CharField(max_length=128)
    character_description = models.CharField(max_length=4000, null=True)
    player = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    character_image = models.ImageField(upload_to='swcs/character_pics/', null=True)
    props = models.ManyToManyField(sheet_property, through='character_properties')
    character_species = models.ForeignKey(species, on_delete=models.CASCADE, null=True)
    # Model config
    objects = character_manager()


class character_properties(models.Model):
    character = models.ForeignKey(character, on_delete=models.CASCADE)
    character_property = models.ForeignKey(sheet_property, on_delete=models.CASCADE)
