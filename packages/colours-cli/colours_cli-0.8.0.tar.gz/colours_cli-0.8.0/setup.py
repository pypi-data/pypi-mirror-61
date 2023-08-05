from setuptools import setup
from colours_cli import __version__

setup(name='colours_cli',
      version=__version__,
      description='CLI using colours_library',
      url='https://gitlab.bitcomp.intra/eryk_malczyk/colourscli',
      author='ErykMalczyk',
      author_email='eryk.malczyk@bitcomp.fi',
      license='some_licence',
      scripts=['bin/colors'],
      packages=['colours_cli'],
      install_requires=[
          'colours_library'
      ],
      tests_require=['pytest',],
      include_package_data=True,
      zip_safe=False)