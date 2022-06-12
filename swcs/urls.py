from swcs import views
from django.urls import path


app_name = 'swcs'
urlpatterns = [
    path('', views.index, name='sw-index'),
    path('roller', views.diceroller, name='sw-roller'),
    path('rest/roll',views.roll, name="sw-rest-roll"),
    path('characters/',views.CharacterListView.as_view(), name="sw-characters"),
    path('characters/create', views.create_character, name="sw-create_character"),
    path('characters/<int:pk>',views.CharacterDetailView.as_view(), name="sw-character"),
 ]
