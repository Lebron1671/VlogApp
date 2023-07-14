from django import forms

class CreateNewArticle(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    content = forms.CharField(label="Content", widget=forms.Textarea)