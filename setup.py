#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages


setup(
    name='v2xpreconfig',
    version='1.0.0',
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
