from swcs import dice, models, forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
# from django.template import loader
# import dice


def index(request):
    return render(request, 'swcs/index.html', context={})


def diceroller(request):
    return render(request, 'swcs/roller.html', context={})


def roll(HttpRequest):
    try:
        dicepool = HttpRequest.GET["dicepool"]
        return JsonResponse(dice.roller(dicepool))
    except :
        return JsonResponse({})

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
