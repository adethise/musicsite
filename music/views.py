from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Song
from .forms import SearchSongsForm

import logging
import urllib.parse
from random import choice

def index(request):
    search_form = SearchSongsForm()
    return render(request, 'music/index.html',
            {'search_form': search_form})

def search(request):
    search_form = SearchSongsForm(request.GET)
    if search_form.is_valid():
        query_key = search_form.cleaned_data['category']
        query_val = search_form.cleaned_data['name']
        query = urllib.parse.urlencode({query_key: query_val})
        url = reverse('random') + '?' + query
        return redirect(url)
    else:
        return render(request, 'music/search_failed.html')

def random(request):
    candidates = Song.get_songs_matching_filter(request.GET)
    url = choice(candidates).get_absolute_url()

    if len(request.GET) > 0:
        url += '?' + request.GET.urlencode()

    return redirect(url)

def song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    filepath = 'music/songs/' + song.filename()
    logging.info('Serving song %s' % song)
    return render(request, "music/song.html",
            {'song': song, 'filepath': filepath})
