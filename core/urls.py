from django.urls import path, include
from django.views.generic.base import TemplateView # new
from core import views

app_name = 'core'
urlpatterns = [
    path("account/", include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='core/index.html'), name='index'),
    path('account/register', views.register, name='register'),
]