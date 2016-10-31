from django.db import models


class Song(models.Model):
    original = models.CharField(max_length = 128)
    name     = models.CharField(max_length = 128)
    artist   = models.CharField(max_length = 128)
    album    = models.CharField(max_length = 128)
    genre    = models.CharField(max_length = 128)
    mime     = models.CharField(max_length = 32)

    def filename(self):
        return self.pk + original[original.rfind('.'):]

    def __str__(self):
        return "%s - %s" % (artist, name)
