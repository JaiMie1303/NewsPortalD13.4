from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class CreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = 'title', 'category', 'content', 'author'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or title.isspace():
            raise forms.ValidationError('Пожалуйста, укажите корректное название.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.isspace():
            raise forms.ValidationError('Пожалуйста, укажите корректное содержимое.')
        return content




