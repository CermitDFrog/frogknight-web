from . import dice
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
# from django.template import loader
# import dice

def index(request):
    return HttpResponse("Character sheet goes here.")

def diceroller(request):
    return render(request, 'swcs/roller.html', context={})

def roll(HttpRequest):
    try:
        dicepool = HttpRequest.GET["dicepool"]
        return JsonResponse(dice.roller(dicepool))
    except :
        return JsonResponse({})