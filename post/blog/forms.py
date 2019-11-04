from django import forms

from .models import BlogPost



class BlogPostForm(forms.Form):
	"""Django Form"""

	title = forms.CharField()
	slug = forms.SlugField()
	content = forms.CharField(widget=forms.Textarea)




class BlogPostModelForm(forms.ModelForm):
	""" Django Model Form """
	class Meta:
		model = BlogPost
		fields = ['title', 'slug', 'image', 'content', 'publish_date']

	def clean_title(self, *args, **kwargs):

		# print(dir(self))
		# print(self.instance)
		title = self.cleaned_data.get('title')
		qs = BlogPost.objects.filter(title__iexact=title)
		
		instance = self.instance
		
		if instance is not None:
			qs = qs.exclude(pk=instance.pk)
		if qs.exists():
			raise forms.ValidationError('The title already exists')

		return title