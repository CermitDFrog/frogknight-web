from django.forms import ModelForm
from django.forms import Textarea
from swcs import models

class create_character(ModelForm):

	class Meta:
		model = models.character
		fields = ("character_name", "character_description", "character_image")
		widgets = {
			'character_description': Textarea(attrs={'cols': 60, 'rows': 10}),
		}
		helptext = {
			'character_image': 'For best results use an image with a 95:100 aspect ratio.'
		}
