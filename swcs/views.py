from swcs import dice, models, forms, serializers
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib import messages
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, 'swcs/index.html', context={})


@login_required
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


class create_character(CreateView, LoginRequiredMixin):
    form_class = forms.character_form
    model = models.character
    template_name = "swcs/create_character.html"

    def form_valid(self, form):
        form.instance.player = self.request.user
        return super().form_valid(form)


class edit_character(UpdateView, LoginRequiredMixin):
    form_class = forms.character_form
    model = models.character
    template_name = "swcs/edit_character.html"

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.player == self.request.user:
            return obj
        raise Http404

    def form_valid(self, form):
        form.instance.player = self.request.user
        return super().form_valid(form)


@login_required
def delete_character(request, pk):
    character = get_object_or_404(models.character, pk=pk)
    if character.player == request.user:
        character.delete()
        messages.success(request, "Character deleted.")
        return redirect('swcs:sw-characters')
    else:
        raise Http404("Character not found.")

# @login_required
# def create_character(request):
    
#     if request.method == "POST":
#         form = forms.character_form(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             character = form.save(commit=False)
#             character.player = request.user
#             character.save()
#             messages.success(request, "Character crerated.")
#             return redirect(reverse('swcs:sw-character', args=(character.id,)))
#         messages.error(request, "Failed to create character")
#     form = forms.character_form()
#     return render(request=request, template_name="swcs/create_character.html", context={"create_character":form})

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
