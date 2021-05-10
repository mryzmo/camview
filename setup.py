
from distutils.core import setup
setup(
  name = 'camview',         # How you named your package folder (MyLib)
  packages = ['camview'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
  author = 'Sebastian Pfaff',                   # Type in your name
  author_email = 'sebastian.pfaff@forbrf.lth.se',      # Type in your E-Mail
  url = 'https://github.com/user/mryzmo',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/mryzmo/camview/archive/refs/tags/0.1.tar.gz',    # I explain this later on
  keywords = ['Thorlabs', 'Santa Barbara Focalplane', 'PLIF'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'PyQt5',
          'pyqtgraph',
          'numpy',
          'matplotlib',
          'scanf',
          'imageio',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'Topic :: Scientific/Engineering :: Image Processing',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)