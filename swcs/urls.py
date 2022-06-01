from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('roller', views.diceroller, name='sw-roller'),
    path('rest/roll',views.roll, name="rest-roll")
]
