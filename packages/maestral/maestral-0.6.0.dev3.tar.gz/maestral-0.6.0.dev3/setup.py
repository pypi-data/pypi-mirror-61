import sys
from setuptools import setup, find_packages

from maestral import __version__

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    # noinspection PyStringFormat
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
Maestral requires Python {}.{} or higher, but you're trying to install
it on Python {}.{}. This may be because you are using a version of pip
that doesn't understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python3 -m pip install --upgrade pip setuptools
    $ python3 -m pip install maestral

""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


setup(
    name='maestral',
    version=__version__,
    description='Open-source Dropbox client for macOS and Linux.',
    url='https://github.com/SamSchott/maestral',
    author='Sam Schott',
    author_email='ss2151@cam.ac.uk',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        'maestral': [
            'resources/*.png',
            ],
        },
    setup_requires=['wheel'],
    install_requires=[
        'atomicwrites',
        'blinker',
        'bugsnag',
        'click>=7.0',
        'dropbox>=9.4.0',
        'keyring>=19.0.0',
        'keyrings.alt>=3.0.0',
        'lockfile',
        'Pyro5>=5.7',
        'requests',
        'rubicon-objc>=0.3.1;sys_platform=="darwin"',
        'u-msgpack-python',
        'watchdog>=0.9.0',
    ],
    extras_require={
        'systemd': [
            'systemd-python',
            'sdnotify'
        ],
        'gui': [
            'maestral-cocoa==0.1.1-dev1;sys_platform=="darwin"',
            'maestral-qt==0.6.1-dev1;sys_platform=="linux"'
        ],
    },
    zip_safe=False,
    entry_points={
      'console_scripts': ['maestral=maestral.cli:main'],
    },
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
