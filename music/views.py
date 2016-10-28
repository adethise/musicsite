from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from random import randrange

def index(request):
    return HttpResponse('Here will be music.')

def random(request):
    song_id = randrange(200)
    return song(request, song_id)

def song(request, song_id):
    return HttpResponse('Here should be song number %s.' % song_id)
