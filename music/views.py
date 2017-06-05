from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q

from .models import Song
from .forms import SearchSongsForm, CategoryForm, SearchForm

import logging
from urllib.parse import urlencode
from random import choice

def index(request):
    search_form = SearchSongsForm(request.GET)
    category_form = CategoryForm(request.GET)
    if category_form.is_valid():
        query = urlencode({'category': category_form.cleaned_data['category']})
        return redirect(reverse('random') + '?' + query)
    elif search_form.is_valid():
        query_key = search_form.cleaned_data['key']
        query_val = search_form.cleaned_data['name']
        query = urlencode({query_key: query_val})
        return redirect(reverse('random') + '?' + query)
    else:
        category_form = CategoryForm()
        search_form = SearchSongsForm()
        return render(request, 'music/index.html',
                {'search_form': search_form, 'category_form': category_form})

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        search = form.cleaned_data['search']
        results = Song.objects.filter(
                Q(name__icontains = search)
                | Q(artist__icontains = search)
                | Q(album__icontains = search)
                | Q(genre__icontains = search)
        )
    else:
        form = SearchForm()
        results = []
    return render(request, 'music/search.html',
            {'form': form, 'songs': results})

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
    logging.info('Serving song %s' % song)

    form = SearchForm(request.GET)
    if form.is_valid():
        search = form.cleaned_data['search']
        results = Song.objects.filter(
                Q(name__icontains = search)
                | Q(artist__icontains = search)
                | Q(album__icontains = search)
                | Q(genre__icontains = search)
        )
    else:
        form = SearchForm()
        results = []

    return render(request, "music/search.html", {
        'song': song,
        'form': form,
        'songs': results
    })
