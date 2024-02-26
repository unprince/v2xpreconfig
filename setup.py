#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages
import re
import sys


if sys.version_info < (3, 6):
    sys.exit("Python 3.6 or newer is required.")

def find_version():
    return re.search(r"^__version__ = '(.*)'$",
                     open('v2xpreconfig/v2xpreconfig.py', 'r').read(),
                     re.MULTILINE).group(1)

setup(
    name='v2xpreconfig',
    version=find_version(),
    license='MIT',
    packages=find_packages(),
    package_data={
        'v2xpreconfig': [
            '*.asn'
        ]
    },
    install_requires=[
        'asn1tools'
    ],
    entry_points={
        'console_scripts': ['v2xpreconfig=v2xpreconfig.__init__:main']
    }
)
