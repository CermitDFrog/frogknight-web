from django.forms import ModelChoiceField, ModelForm, Textarea, Select
from swcs import models

class create_character(ModelForm):
	character_species = ModelChoiceField(
		queryset=models.species.objects.all(),
		to_field_name="species_name",
		widget=Select(attrs={"onChange":'updateSpecies()'}))

	class Meta:
		model = models.character
		fields = ("character_name", "character_description", 
				  "character_image","character_species")
		widgets = {
			'character_description': Textarea(attrs={'cols': 60, 'rows': 10})
		}
		helptext = {
			'character_image': 'For best results use an image with a 95:100 aspect ratio.'
		}
