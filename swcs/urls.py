from django.urls import path

from . import views

app_name = 'swcs'
urlpatterns = [
    path('', views.index, name='sw-index'),
    path('roller', views.diceroller, name='sw-roller'),
    path('rest/roll',views.roll, name="sw-rest-roll")
]
