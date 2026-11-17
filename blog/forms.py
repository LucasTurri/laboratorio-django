from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        labels = {
            "title": "Título",
            "content": "Conteúdo em HTML",
        }
        widgets = {
            "content": forms.Textarea(attrs={"rows": 8, "cols": 60}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": "Comentário"}