import os
from glob import glob
import zipfile
# finally using the six library like a big boy.
# don't be surprised if your editor says there is no "urlopen." six is wonky like that.
from six.moves.urllib.request import urlopen

from speedyvpn.utils.custom_errors import ImpossibleError

def check_ovpn_dir(root_dir_path):
    """
    This function checks to see if the .speedyvpn/ directory is present inside the users HOME directory.
      - If it IS NOT, it creates it or throws an error if there is a name-conflict with a file.
      - If it IS, it clears it out.

    :param root_dir_path: default is the users $HOME env-variable (%HOME% on windows).

    :return: the absolute path of the .speedyvpn/ directory
    """
    # os.path.realpath() gives us an abs-path from a relative-path when applicable. It's never not safe to use...
    ovpn_dir_path = os.path.realpath(os.path.join(root_dir_path, '.speedyvpn'))

    # 3 things are possible. Handle each.
    if not os.path.exists(ovpn_dir_path):
        os.mkdir(ovpn_dir_path)
        # let's prevent anyone but us from using this.
        os.chmod(ovpn_dir_path, 700)
        # cuz why not. It will be useful later.
        return ovpn_dir_path

    elif os.path.exists(ovpn_dir_path) and os.path.isfile(ovpn_dir_path):
        raise FileExistsError('you have a FILE named OVPN in the root dir your specified. \nMove or remove it.')

    elif os.path.exists(ovpn_dir_path) and os.path.isdir(ovpn_dir_path):
        ovpn_files = glob(os.path.join(ovpn_dir_path, '*.ovpn'))
        zip_files = glob(os.path.join(ovpn_dir_path, 'zip*'))
        if ovpn_files:
            [os.remove(i) for i in ovpn_files]
        if zip_files:
            [os.remove(i) for i in zip_files]
        # cuz why not. It will be useful later.
        return ovpn_dir_path

    else:
        raise ImpossibleError('You broke everything.')

def download_and_extract_nord_zipfile(ovpn_dir_path):
    """
    This function retrieves NordVPN's zipfile, de-serializes & saves it.
    Then it extracts the contents.

    :param ovpn_dir_path: efault is the users {$HOME}/OVPN/ (%HOME%\OVPN\ on windows)

    :return: NUTHIN'
    """
    zip_data = urlopen('https://nordvpn.com/api/files/zip').read()
    zipfile_path = os.path.join(ovpn_dir_path, 'zipfile.zip')
    with open(zipfile_path, 'wb+') as nord_zipfile:
        nord_zipfile.write(zip_data)
    # sanity check
    assert os.path.exists(zipfile_path)
    # lololol This could be more than one line...buttfuckit
    #TODO: also this can b dangerous AF. Need to make some checks before deserializing.
    zipfile.ZipFile(zipfile_path).extractall(ovpn_dir_path)




def update(root_dir_path=os.environ['HOME']):
    assert os.path.exists(root_dir_path) and os.path.isdir(root_dir_path), 'please provide a valid starting directory.'
    # The following function should give back a longer path.
    ovpn_dir_pth = check_ovpn_dir(root_dir_path)
    # potentially unnecessary assert statement, but a good check.
    assert os.path.exists(ovpn_dir_pth)
    download_and_extract_nord_zipfile(ovpn_dir_pth)



if __name__ == '__main__':
    update()


