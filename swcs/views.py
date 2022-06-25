from django import views
from swcs import dice, models, forms, serializers
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from rest_framework import viewsets
# from django.template import loader
# import dice


def index(request):
    return render(request, 'swcs/index.html', context={})


def diceroller(request):
    if request.user.is_authenticated:
        context = {"characters": models.character.objects.user_characters(request.user)}
        return render(request, 'swcs/roller.html', context=context)
    else:
        return render(request, 'swcs/roller.html', context={})


def roll(HttpRequest):
    try:
        dicepool = HttpRequest.GET["dicepool"]
        character_name = HttpRequest.GET["character"]
        return JsonResponse(dice.roller(dicepool, character_name))
    except Exception as e:
        print(e)
        return {}


@login_required
def create_character(request):
    
    if request.method == "POST":
        form = forms.create_character(request.POST, request.FILES)
        if form.is_valid():
            character = form.save(commit=False)
            character.player = request.user
            print(character.__dict__)
            character.save()
            print('Saved.')
            messages.success(request, "Character crerated.")
            return redirect(reverse('swcs:sw-character', args=(character.id,)))
        messages.error(request, "Failed to create character")
    form = forms.create_character()
    return render(request=request, template_name="swcs/create_character.html", context={"create_character":form})

class CharacterListView(LoginRequiredMixin, ListView):
    model = models.character
    template_name = 'swcs/characters.html'
    context_object_name = 'characters'

    def get_queryset(self):
        return models.character.objects.user_characters(
            self.request.user)


class CharacterDetailView(LoginRequiredMixin, DetailView):
    model = models.character
    template_name = 'swcs/character.html'
    context_object_name = 'character'


class SpeciesViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'species_name'
    queryset = models.species.objects.all()
    serializer_class = serializers.species_serializer
