from django import forms
from .models import Post, Image, Comment

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Post
        fields = ['content']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_url']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
