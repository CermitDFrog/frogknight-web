from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import NewUserForm, CoreUserChangeForm
from core.models import CoreUser

# admin.site.register(CoreUser)# Register your models here.

class CoreUserAdmin(UserAdmin):
    add_form = NewUserForm
    form = CoreUserChangeForm
    model = CoreUser
    list_display = ["email", "username",]

admin.site.register(CoreUser, CoreUserAdmin)