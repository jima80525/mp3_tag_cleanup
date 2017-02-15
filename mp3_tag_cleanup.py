#! /usr/bin/env python
""" Simple script to clean up some MP3 tags using mutagen.
    Makes the 'title' tag be "Track_01" to match the track number.  (Assumes
    that all tracks are numbered properly.  Use EasyTag to do that.)
    Also renames the file to be Track_01.mp3.
    Not production ready - just basic functionality. """
import os
import subprocess

from mutagen.easyid3 import EasyID3


def fix_single_file_name_and_title(path, filename, fake):
    """ takes full path and filename information and cleans up that
    file.  Fake flag tests but does not modify the file. """
    fullname = os.path.join(path, filename)
    track = EasyID3(fullname)
    # build the new track name by getting the number
    # Tracks will be named Track_xx where xx is always a two-digit number
    # with zero-padding if needed.
    track_num = track.get('tracknumber')[0]
    # print("THIS IS TRACK NUM before ", track_num)
    if '/' in track_num:
        track_num = track_num.split('/')[0]
    if "Chapter" in track_num:
        print("THIS IS TRACK NUM AFTER ", track_num)
        print(fullname)
    track_name = u"Track_{:02d}".format(int(track_num))
    if track['title'][0] != track_name:
        print("Changing title from {} to {}".format(track['title'][0],
                                                    track_name))
    track['title'] = track_name
    if not fake:
        track.save()

    # now create a new filename and move the file
    valid_filename = u"{0}/{1}.mp3".format(path, track_name)
    if fullname != valid_filename:
        print("moving {} to {}".format(fullname, valid_filename))
        if not fake:
            subprocess.call(["/bin/mv", fullname, valid_filename])


if __name__ == "__main__":
    PATH = os.getcwd()
    for DIRNAME, _, FILELIST in os.walk(PATH):
        for FILENAME in FILELIST:
            if FILENAME.endswith(".mp3"):
                fix_single_file_name_and_title(DIRNAME, FILENAME, False)
