from django import forms

from .models import Song

class SearchSongsForm(forms.Form):

    SEARCH_KEYS = [('artist', 'Artist'), ('source', 'Source')]

    name = forms.CharField(label = 'Name', max_length = 128)
    key  = forms.ChoiceField(label = 'Search in', choices = SEARCH_KEYS)

class CategoryForm(forms.Form):

    CATEGORIES = [
            ('Anime', 'Anime'),
            ('Games', 'Games'),
            ('Nightcore', 'Nightcore'),
            ('Vocaloid', 'Vocaloid'),
    ]

    category = forms.ChoiceField(choices = CATEGORIES)

class SearchForm(forms.Form):

    search = forms.CharField(required = False)
