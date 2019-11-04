
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.utils import timezone
from django.shortcuts import (
	render, 
	get_object_or_404,
	redirect
)

from .models import BlogPost, UserComment
from .forms import BlogPostForm, BlogPostModelForm

# Create your views here.

def blog_post_detail_page(request, slug):
	
	# try:
	# 	blog = BlogPost.objects.get(id=post_id)		
	# except BlogPost.DoesNotExist:
	# 	raise Http404
	# blog = BlogPost.objects.get(id=post_id)
	# blog = get_object_or_404(BlogPost, slug=slug)
	
	blog = BlogPost.objects.filter(slug=slug)
	
	if blog.count() >= 1:
		blog = blog.first()
		comments = blog.usercomment_set.all()
	else:
		comments = blog.usercomment_set.all()

	template_name = "blog/detail.html"
	context = {"object":blog, "comments":comments}
	return render(request, template_name, context)



def blog_post_list_view(request):
	"""
	List view of posts
	"""
	# now = timezone.now()
	# qs = BlogPost.objects.all()[:5]
	# qs = BlogPost.objects.filter(publish_date__lte=now)
	qs = BlogPost.objects.all().published()

	if request.user.is_authenticated:
		my_qs = BlogPost.objects.filter(user=request.user)
		# remove duplicates from both queries
		qs = (qs | my_qs).distinct()

	template_name = "blog/list.html"
	context = {"objects":qs}
	return render(request, template_name, context)



"""
Loging required URL defined in settings file
"""
# @login_required
@staff_member_required
def blog_post_create_view(request):

	# if not request.user.is_authenticated:
	# 	return render(request, 'blog/not-authenticated.html', context)

	form = BlogPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		# blog = BlogPost.objects.create(**form.cleaned_data)
		obj = form.save(commit=False)
		obj.user = request.user
		obj.save()
		form = BlogPostModelForm()

	template_name = "blog/form.html"
	context = {"form":form, "title":"Blog form page"}
	return render(request, template_name, context)



@staff_member_required
def blog_post_update_view(request, slug):

	blog = get_object_or_404(BlogPost, slug=slug)
	form = BlogPostModelForm(request.POST or None, instance=blog)

	if form.is_valid():
		form.save()

	template_name = "blog/form.html"
	context = {"form":form, "title":f"Update | {blog.title}"}
	return render(request, template_name, context)



@staff_member_required
def blog_post_delete_view(request, slug):

	blog = get_object_or_404(BlogPost, slug=slug)

	if request.method == "POST":
		blog.delete()
		return redirect("/blog/")

	template_name = "blog/delete.html"
	context = {"title":blog.title}
	return render(request, template_name, context)



def blog_post_retrieve_view(request):
	
	template_name = "blog/retrieve.html"
	context = {"object":""}
	return render(request, template_name, context)


def comment_create(request, slug):
	# Need to implement Django forms for better security 
	formdata = request.POST
	# print(formdata)
	# print(formdata["email"])

	blog= get_object_or_404(BlogPost, slug=slug)
	
	obj= UserComment(
			blogpost=blog,
			email=formdata["email"],
			firstname=formdata["firstname"],
			lastname=formdata["lastname"],
			comment=formdata["comment"]
		)
	obj.save()

	# context = {"message":""}
	# return render(request, template_name, context)
	return redirect(f'/blog/{slug}/')