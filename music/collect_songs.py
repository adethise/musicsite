#!/usr/bin/env python3

"""
This script's goal is to automatize collecting songs files and storing
their metadata in the django database.

Files lacking song metadata information 'name' or 'artist' will be ignored.

Files will be copied in the development static directory. It is still
necessary to run `python manage.py collectstatic` to use them in production.
"""


# system and filesystem
import os
import sys

# django
import django
from django.contrib.staticfiles.storage import staticfiles_storage
from music.models import Song

# utilities
import argparse
import mutagen
import shutil


django.setup()
# add the parent directory to the python path to import settings
sys.path.append(os.path.dirname(os.getcwd()))
os.environ['DJANGO_SETTINGS_MODULE'] = 'musicsite.settings'

static_url = staticfiles_storage.url # shortcut


def reset():
    print('You asked to reset the previously collected songs.')
    print('This will erase the content of %s ' % static_url('music/songs/')
            + 'and the songs in the database.')
    print('Are you really sure you want to do this ?')

    if not confirm():
        print('Suppression cancelled.')
        return

    raise NotImplementedError

def confirm():
    """
    Return true if the user confirm the action, false otherwise.

    The following inputs are accepted:
    - True values are y, yes, t, true, on and 1
    - False values are n, no, f, false, off and 0.
    """
    from distutils.util import strtobool
    while True:
        answer = input('(type "yes" or "no") ')
        try:
            return strtobool(answer)
        except ValueError:
            return confirm()

def collect(dirname):
    """
    Collects all music files in directory.

    dirname -- path to a dir containing the songs
    """
    files = os.listdir(dirname)
    for i, filename in enumerate(files):
        if args.verbose:
            sys.stdout.write('\rCollecting songs in %s (%d%%)'
                    % (dirname, 100 * (i+1) / len(files)))
            sys.stdout.flush()
        try:
            collect_song(dirname, filename)
        except ValueError as e:
            print(e)

def collect_song(dirname, filename):
    """
    Collect a single song.

    dirname  -- name of the containing directory
    filename -- name of the song file

    Throws ValueError if the file doesn't exist, isn't a song,
    or lacks metadata information 'name' and 'artist'.
    """
    filepath = os.path.join(dirname, filename)

    try:
        raw = mutagen.File(filepath)
        song = Song(
                original = filename,
                name     = raw.get('title')[0],
                artist   = raw.get('artist')[0],
                genre    = raw.get('genre', [''])[0],
                album    = raw.get('album', [''])[0],
                mime     = 'audio/ogg')
        song.save()
    except Exception as e:
        raise ValueError('Could not collect file %s' % filepath)

    static_filepath = static_url('music/songs/' + song.filename())
    shutil.copy(filepath, os.getcwd() + static_filepath)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description = 'Read all music files in the given directories ' +\
            'and add them to the database and the static files directory')
    parser.add_argument('-d', '--delete', action = 'store_true',
            help = 'remove the previous content')
    parser.add_argument('-v', '--verbose', action = 'store_true',
            help = 'verbose mode')
    parser.add_argument('dirs', nargs = '+', help = 'music files directory')
    args = parser.parse_args()

    if args.reset:
        reset()

    for dirname in args.dirs:
        collect(dirname)