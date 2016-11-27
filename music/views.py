from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from music.models import Song

import logging
from random import choice


def index(request):
    return HttpResponseRedirect('random')

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
        candidates = candidates.filter(source_contains=source)

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
