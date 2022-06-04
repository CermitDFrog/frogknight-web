from django.contrib.auth import login, authenticate
from core.forms import NewUserForm
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("core:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})

def view_404(request, *ags, **kwargs):
    return render(request, 'core/404.html', status=404)
