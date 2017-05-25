# encoding: utf-8

import os
import sys
import codecs
from setuptools import setup
import tornado_scaffold

__DIR__ = os.path.abspath(os.path.dirname(__file__))


def read(filename):
    """Read and return `filename` in root dir of project and return string"""
    return codecs.open(os.path.join(__DIR__, filename), "r").read()

install_requires = [
    "tornado",
    "Tornado-JSON",
    "peewee",
    "bcrypt",
    "psycopg2"  # use postgresql
]
long_description = read("README.md")

setup(
    name="tornado_scaffold",
    version=tornado_scaffold.__version__,
    url="https://github.com/zxzhang5/tornado_scaffold",
    license="MIT License",
    author="Zhang Zhi Xiang",
    description="A scaffold project based on Tornado",
    long_description=long_description,
    packages=["tornado_scaffold"],
    install_requires=install_requires,
    data_files=[
        # Populate this with any files config files etc.
    ],
    classifiers=[   # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Framework :: Tornado",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ]
)
