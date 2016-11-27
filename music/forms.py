from django import forms

from .models import Song

class SearchSongsForm(forms.Form):

    SEARCH_CATEGORIES = [("artist", "Artist"), ("source", "Source")]

    name     = forms.CharField(max_length = 128)
    category = forms.ChoiceField(choices = SEARCH_CATEGORIES)

    def clean(self):
        super(SearchSongsForm, self).clean()

        name     = self.cleaned_data['name']
        category = self.cleaned_data['category']

        if len(Song.get_songs_matching_filter({category: name})) == 0:
            raise forms.ValidationError(
                    "Your query didn't return any result."
            )
