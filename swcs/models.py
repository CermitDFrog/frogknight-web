from django.db import models
from django.conf import settings
from django.urls import reverse


def get_default_skills():
    return {"Astrogation": {"Attribute": "Intellect", "Value": 0},
            "Athletics": {"Attribute": "Brawn", "Value": 0},
            "Brawl": {"Attribute": "Brawn", "Value": 0},
            "Charm": {"Attribute": "Presence", "Value": 0},
            "Coercion": {"Attribute": "Willpower", "Value": 0},
            "Computers": {"Attribute": "Intellect", "Value": 0},
            "Cool": {"Attribute": "Presence", "Value": 0},
            "Coordination": {"Attribute": "Agility", "Value": 0},
            "Core Worlds": {"Attribute": "Intellect", "Value": 0},
            "Deception": {"Attribute": "Cunning", "Value": 0},
            "Discipline": {"Attribute": "Willpower", "Value": 0},
            "Education": {"Attribute": "Intellect", "Value": 0},
            "Gunnery": {"Attribute": "Agility", "Value": 0},
            "Leadership": {"Attribute": "Presence", "Value": 0},
            "Lightsaber": {"Attribute": "Brawn", "Value": 0},
            "Lore": {"Attribute": "Intellect", "Value": 0},
            "Mechanics": {"Attribute": "Intellect", "Value": 0},
            "Medicine": {"Attribute": "Intellect", "Value": 0},
            "Melee": {"Attribute": "Brawn", "Value": 0},
            "Negotiation": {"Attribute": "Presence", "Value": 0},
            "Outer Rim": {"Attribute": "Intellect", "Value": 0},
            "Perception": {"Attribute": "Cunning", "Value": 0},
            "Piloting (Planetary)": {"Attribute": "Agility", "Value": 0},
            "Piloting (Space)": {"Attribute": "Agility", "Value": 0},
            "Piloting (Heavy)": {"Attribute": "Agility", "Value": 0},
            "Ranged (Heavy)": {"Attribute": "Agility", "Value": 0},
            "Ranged (Light)": {"Attribute": "Agility", "Value": 0},
            "Resilience": {"Attribute": "Brawn", "Value": 0},
            "Skullduggery": {"Attribute": "Cunning", "Value": 0},
            "Social": {"Attribute": "Presence", "Value": 0},
            "Stealth": {"Attribute": "Agility", "Value": 0},
            "Streetwise": {"Attribute": "Cunning", "Value": 0},
            "Subterfuge": {"Attribute": "Cunning", "Value": 0},
            "Survival": {"Attribute": "Cunning", "Value": 0},
            "Vigilance": {"Attribute": "Willpower", "Value": 0},
            "Xenology": {"Attribute": "Intellect", "Value": 0}}


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
    species_image = models.ImageField(
        upload_to='swcs/species_pics/', null=True)
    props = models.ManyToManyField(
        sheet_property, through='species_properties')

    def __str__(self):
        return self.species_name


class species_properties(models.Model):
    species = models.ForeignKey(species, on_delete=models.CASCADE)
    species_property = models.ForeignKey(
        sheet_property, on_delete=models.CASCADE)


class character(models.Model):
    # Fields
    character_name = models.CharField(max_length=128)
    character_description = models.CharField(max_length=4000, null=True)
    player = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    character_image = models.ImageField(
        upload_to='swcs/character_pics/', null=True, blank=True)
    props = models.ManyToManyField(
        sheet_property, through='character_properties')
    character_species = models.ForeignKey(
        species, on_delete=models.CASCADE, null=True)
    character_skills = models.JSONField(
        default=get_default_skills, null=True)

    # Model config
    objects = character_manager()

    def get_absolute_url(self):
        return reverse('swcs:sw-character', args=(self.id,))


class character_properties(models.Model):
    character = models.ForeignKey(character, on_delete=models.CASCADE)
    character_property = models.ForeignKey(
        sheet_property, on_delete=models.CASCADE)
