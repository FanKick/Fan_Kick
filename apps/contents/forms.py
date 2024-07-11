from django import forms
from .models import Post, Image

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user', 'team', 'title', 'content']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_url']