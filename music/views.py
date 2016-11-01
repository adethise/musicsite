from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from music.models import Song

import logging
from random import choice


def index(request):
    return HttpResponseRedirect('random')

def random(request):
    return redirect(choice(Song.objects.all()))

def song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    filepath = 'music/songs/' + song.filename()
    logging.info('Serving song %s' % song)
    return render(request, "music/song.html",
            {'song': song, 'filepath': filepath})
