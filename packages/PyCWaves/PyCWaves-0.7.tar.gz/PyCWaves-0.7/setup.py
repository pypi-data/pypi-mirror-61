from distutils.core import setup
setup(
  name = 'PyCWaves',         # How you named your package folder (MyLib)
  packages = ['PyCWaves'],   # Chose the same as "name"
  version = '0.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Object-Oriented version of PyWaves library',   # Give a short description about your library
  author = 'mortimer',                   # Type in your name
  author_email = 'info@mortysnode.nl',      # Type in your E-Mail
  url = 'https://github.com/iammortimer/PyCWaves',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/iammortimer/PyCWaves/archive/v0.7.tar.gz',    # I explain this later on
  keywords = ['WAVES', 'CLASS', 'PyWaves'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'python-axolotl-curve25519',
          'pyblake2',
          'base58',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
