#!/usr/bin/env python3

import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'musicsite.settings'
sys.path.append(os.path.dirname(os.getcwd()))

import django
django.setup()
from django.contrib.staticfiles.storage import staticfiles_storage
from music.models import Song

import argparse
import mutagen, shutil

static_url = staticfiles_storage.url

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
    from distutils.util import strtobool
    while True:
        answer = input('(type "yes" or "no") ')
        try:
            return strtobool(answer)
        except ValueError:
            return confirm()

def collect(dirname):
    files = os.listdir(dirname)
    for i, filename in enumerate(files):
        if args.verbose:
            sys.stdout.write('\rCollecting songs in %s (%d%%)' 
                    % (dirname, 100 * (i+1) / len(files)))
            sys.stdout.flush()
        collect_song(dirname, filename)

def collect_song(dirname, filename):
    filepath = os.path.join(dirname, filename)

    raw = mutagen.File(filepath)
    song = Song(
            original = filename,
            name     = raw.get('title')[0],
            artist   = raw.get('artist')[0],
            genre    = raw.get('genre', [''])[0],
            album    = raw.get('album', [''])[0],
            mime     = 'audio/ogg')
    song.save()
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
