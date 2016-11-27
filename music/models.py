from django.db import models


class Song(models.Model):
    original = models.CharField(max_length = 128)
    name     = models.CharField(max_length = 128)
    artist   = models.CharField(max_length = 128)
    genre    = models.CharField(max_length = 128)
    album    = models.CharField(max_length = 128)
    mime     = models.CharField(max_length = 32)

    def filename(self):
        return str(self.pk) + self.original[self.original.rfind('.'):]

    def get_absolute_url(self):
        from django.shortcuts import reverse
        return reverse('song', args=[self.pk])

    def __str__(self):
        return "%s - %s" % (self.artist, self.name)

    @staticmethod
    def get_songs_matching_filter(query):
        candidates = Song.objects.all()

        title = query.get("title", None)
        if title:
            candidates = candidates.filter(title__contains=title)

        artist = query.get("artist", None)
        if artist:
            candidates = candidates.filter(artist__contains=artist)

        category = query.get("category", None)
        if category:
            candidates = candidates.filter(genre__iexact=category)

        source = query.get("source", None)
        if source:
            candidates = candidates.filter(album__contains=source)

        return candidates
