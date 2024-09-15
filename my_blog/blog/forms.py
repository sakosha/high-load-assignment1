from django import forms

from .models import Comment
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'content')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
