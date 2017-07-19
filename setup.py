from setuptools import setup, find_packages
setup(name='speedyvpn',
      version='0.0.2',

      #TODO: U DO THIS BEEEEEYATCH
      description='THIS IS FOR YOU ZACH',

      url='https://PLEASEPLEASEPLEASE.buythingsfrom.us',
      author='Zachary Estela, Robert Truxal',
      author_email='z@arcel.io, smashsmashsmashsmash@buythingsfrom.us',
      license='MIT-like (see LICENCE file)',

      packages=find_packages(),

      include_package_data=True,
      package_dir={'shell_scripts' : 'speedyvpn/shell_scripts'},
      package_data={'shell_scripts' : ['shell_scripts/*.sh']},

      entry_points={
        'console_scripts' : [
            'speedyvpn = speedyvpn.__main__:main'
        ]
      },

      install_requires= [
            'azure',
            'msrest',
            'msrestazure',
      ],

      zipsafe=False
      )