from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Song
from .forms import SearchSongsForm, CategoryForm

import logging
from urllib.parse import urlencode
from random import choice

def index(request):
    search_form = SearchSongsForm()
    category_form = CategoryForm()
    return render(request, 'music/index.html',
            {'search_form': search_form, 'category_form': category_form})

def search(request):

    form = CategoryForm(request.GET)
    if form.is_valid():
        query= urlencode({'category': form.cleaned_data['category']})
        url = reverse('random') + '?' + query
        return redirect(url)

    form = SearchSongsForm(request.GET)
    if form.is_valid():
        query_key = form.cleaned_data['key']
        query_val = form.cleaned_data['name']
        query = urlencode({query_key: query_val})
        url = reverse('random') + '?' + query
        return redirect(url)

def random(request):
    candidates = Song.objects.all()

    title = request.GET.get("title", None)
    if title:
        candidates = candidates.filter(title__contains=title)

    artist = request.GET.get("artist", None)
    if artist:
        candidates = candidates.filter(artist__contains=artist)

    category = request.GET.get("category", None)
    if category:
        candidates = candidates.filter(genre__iexact=category)

    source = request.GET.get("source", None)
    if source:
        candidates = candidates.filter(album__contains=source)

    if len(candidates) == 0:
        return render(request, 'music/search_failed.html')
    else:
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
