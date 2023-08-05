# -* coding: utf-8 *-
from setuptools import setup, find_packages
from os import path
from io import open

import swapietl


HERE = path.abspath(path.dirname(__file__))


with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='swapietl',
    version=swapietl.__version__,
    description='Star Wars API ETL - YouGov',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dgarana/swapietl',
    author='David Garaña',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': ['swapietl=swapietl.cli:main'],
    },
    packages=find_packages(exclude=['contrib', 'docs', 'test']),
    # Hardcoded requirements due issues when parsing with pip
    install_requires=[
        "vulcano",
        "coloredlogs",
        "swapi",
        "requests",
    ]
)
