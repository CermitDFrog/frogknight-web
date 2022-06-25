from swcs.models import species, character
from rest_framework import serializers

class species_serializer(serializers.ModelSerializer):
    class Meta:
        model = species
        fields = "__all__"
