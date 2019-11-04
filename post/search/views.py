from django.shortcuts import render

from .models import SearchQuery
from blog.models import BlogPost
# Create your views here.

def search_view(request):
	
	query = request.GET.get('q', None)
	user = None
	context = {"query":query}

	if request.user.is_authenticated:
		user = request.user

	if query is not None:
		SearchQuery.objects.create(user=user, query=query)
		qs = BlogPost.objects.search(query=query)	
		context["results"] = qs

	template_name = "search/view.html"
	
	return render(request, template_name, context)