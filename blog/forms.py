# blog/forms.py

from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class PostUpdateForm(forms.ModelForm):
    image = forms.FileField(required=False)  # This makes the input a file upload

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']

class PostCreateForm(forms.ModelForm):
    image = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']