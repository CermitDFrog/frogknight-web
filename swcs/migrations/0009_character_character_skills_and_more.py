# Generated by Django 4.0.4 on 2022-07-10 03:31

from django.db import migrations, models
import swcs.models


class Migration(migrations.Migration):

    dependencies = [
        ('swcs', '0008_species_species_agility_species_species_brawn_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='character_skills',
            field=models.JSONField(default=swcs.models.get_default_skills, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='character_image',
            field=models.ImageField(blank=True, null=True, upload_to='swcs/character_pics/'),
        ),
    ]
