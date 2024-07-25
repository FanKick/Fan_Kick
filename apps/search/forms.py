from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Player', max_length=100)
