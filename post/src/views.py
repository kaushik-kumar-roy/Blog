from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib.auth import authenticate

from .forms import ContactForm

def home_page(request):
	return render(request, "home.html",{"title":"Home page"})

def contact_page(request):

	form = ContactForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)
		form = ContactForm()

	return render(request, "form.html",{
		"title":"Contact page",
		"form":form
	})

def about_page(request):
	return render(request, "about.html",{"title":"About page"})


def example_page(request):
	context = {"title":"Example Title"}
	template_name = "example.txt"
	template_obj = get_template(template_name)
	rendered_string = template_obj.render(context)
	return render(request, "home.html", {"title":rendered_string})

"""
# Account login actions
#
"""
def accounts_login(request):

	formdata = request.POST
	print(formdata)
	print(formdata['email'])
	print(formdata['password'])

	user = authenticate(
		email=formdata['email'], 
		password=formdata['password']
	)

	if user is not None:
		return redirect('')
	else:
		return render(request, "login.html", {"title":"Login page"})

def accounts_logout(request):
	data = request.POST
	print(data)
	return render(request, "signup.html", {"title":"Login page"})

def accounts_create(request):
	data = request.POST
	print(data)
	return render(request, "signup.html", {"title":"Login page"})
