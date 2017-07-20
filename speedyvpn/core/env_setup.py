import os
from glob import glob
import zipfile
import urllib

from speedyvpn.utils.custom_errors import ImpossibleError

def check_ovpn_dir(root_dir_path):
    # os.path.realpath() gives us an abs-path from a relative-path when applicable. It's never not safe to use...
    ovpn_dir_path = os.path.realpath(os.path.join(root_dir_path, 'OVPN'))

    # 3 things are possible. Handle each.
    if not os.path.exists(ovpn_dir_path):
        os.mkdir(ovpn_dir_path, mode=755)
        return 0
    elif os.path.exists(ovpn_dir_path) and os.path.isfile(ovpn_dir_path):
        raise FileExistsError('you have a FILE named OVPN in the root dir your specified. \nMove or remove it.')
    elif os.path.exists(ovpn_dir_path) and os.path.isdir(ovpn_dir_path):
        ovpn_files = glob(os.path.join(ovpn_dir_path, '*.ovpn'))
        zip_files = glob(os.path.join(ovpn_dir_path, 'zip*'))
        if ovpn_files:
            [os.remove(i) for i in ovpn_files]
        if zip_files:
            [os.remove(i) for i in zip_files]
        return 0
    else:
        raise ImpossibleError('You broke everything.')


def main(root_dir_path=os.getcwd()):
    assert os.path.exists(root_dir_path) and os.path.isdir(root_dir_path), 'please provide a valid starting directory.'
    should_be_zero = check_ovpn_dir(root_dir_path)
    if should_be_zero is not 0:
        raise ImpossibleError()

if __name__ == '__main__':
    main()


