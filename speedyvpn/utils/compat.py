from sys import getfilesystemencoding

def sysencode(string):
    return string.encode(getfilesystemencoding())
