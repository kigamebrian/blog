from django import forms

from .models import Post,Comment



class PostForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=[
		"title",
		"content",
		"image",
		]

class CommentForm(forms.Form):
	content_type =forms.CharField(widget=forms.HiddenInput)
	object_id =forms.IntegerField(widget=forms.HiddenInput)
	#parent_id =forms.IntegerField(widget.HiddenInput)
	content =forms.CharField(widget=forms.Textarea)

	