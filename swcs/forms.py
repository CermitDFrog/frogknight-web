from django.forms import HiddenInput, IntegerField, ModelChoiceField, ModelForm, Textarea, Select
from swcs import models


class character_form(ModelForm):
    character_species = ModelChoiceField(
        queryset=models.species.objects.all(),
        to_field_name="species_name",
        widget=Select(attrs={"onChange":'updateSpecies()'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for skill in models.get_default_skills():
            self.fields[skill] = IntegerField(initial=0,max_value=5, min_value=0)

    class Meta:
        model = models.character
        fields = ["character_name", "character_description", 
                  "character_image","character_species", "character_skills"]
        widgets = {
            'character_description': Textarea(attrs={'cols': 60, 'rows': 10}),
            'character_skills': HiddenInput()
        }
        helptext = {
            'character_image': 'For best results use an image with a 95:100 aspect ratio.'
        }

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['character_skills'] = models.get_default_skills()
        for skill in self.cleaned_data['character_skills']:
            self.cleaned_data['character_skills'][skill]["Value"] = cleaned_data[skill]
        return cleaned_data
