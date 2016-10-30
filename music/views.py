from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404

from random import randrange

NUM_SONGS = 8 # this horrible hack will be removed once the model is done

def index(request):
    return HttpResponseRedirect('random')

def random(request):
    song_id = randrange(NUM_SONGS)
    return redirect('song', song_id=song_id)

def song(request, song_id):
    if int(song_id) not in range(NUM_SONGS):
        raise Http404("Song does not exist.")
    else:
        song_name = song_id
        song_url1 = 'music/songs/%s.ogg' % song_id
        song_url2 = 'music/songs/%s.opus' % song_id
        song_mime = 'audio/ogg'
        
        return render(request, "music/song.html", locals())
