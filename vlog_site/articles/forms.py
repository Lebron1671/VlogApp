from django import forms
from django.core.exceptions import ValidationError

from .models import *

class AddArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Category is not selected'
    class Meta:
        model=Article
        fields=['article_title', 'article_content', 'category', 'photo']
        widgets = {
            'article_title': forms.TextInput(attrs={'class': 'form-input'}),
            'article_content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }