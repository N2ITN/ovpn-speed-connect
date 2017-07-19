from ._version import __version__

import os

# this is part of the convoluted way python makes you put non-python files in pip-installable packages.
# it's dumb.
def get_scripts(path):
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    return os.path.realpath(os.path.join(_ROOT, 'shell_scripts', path))


# NO. BAD WILDCARDS.
__all__ = [
    'speedyvpn',
]
