import os, sys
from setuptools import find_packages, setup
sys.path.append('./aos')
from aos import __title__, __version__, __description__, __url__, __author__, __email__

LONG_DESC = open('pypi_readme.rst').read()
LICENSE = open('LICENSE').read()

install_requires = [
    'pyserial',
    'esptool',
    'scons',
    'requests',
    'click',
    'paho-mqtt',
    'progressbar2',
    'configparser',
]

setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=LONG_DESC,
    url=__url__,
    author=__author__,
    author_email=__email__,
    license=LICENSE,
    python_requires='>=2.7',
    packages=find_packages(),
    package_dir={'aos':'aos'},
    package_data={'aos': ['.vscode/*']},
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'aos=aos.__main__:main',
            'aos-cube=aos.__main__:main',
        ]
    },
)
