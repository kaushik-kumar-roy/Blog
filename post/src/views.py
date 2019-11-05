from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib.auth import (
	authenticate, 
	login, 
	logout
)

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

	print(request.POST)
	print(f"post data : {bool(request.POST)}")
	
	context = {"title":"Login page"}
	# check if POST dict is empty
	post_data = bool(request.POST)

	if request.POST is None or post_data==False:
		template_name = "login.html"
		return render(request, template_name, context)

	if request.POST["username"]=="" or request.POST["password"]=="":
		context['message']= "We received empty values. Please provide the correct credentials"
		template_name = "login.html"
		return render(request, template_name, context)

	# Authenticate and redirect the user
	formdata = request.POST
	user = authenticate(
		request,
		username=formdata['username'], 
		password=formdata['password']
	)

	if user is not None:
		login(request, user)		
		return redirect("/", {"title": "Home page"})		
	else:
		context['message']= "We didn't find any account with the provided credentials."
		template_name = "login.html"
		return render(request, template_name, context)

def accounts_logout(request):
	logout(request)
	return redirect("/", {"title": "Home page"})

def accounts_create(request):
	data = request.POST
	print(data)
	return render(request, "signup.html", {"title":"Login page"})
