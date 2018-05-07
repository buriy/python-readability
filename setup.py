#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

lxml_requirement = "lxml"
if sys.platform == 'darwin':
    import platform
    mac_ver = platform.mac_ver()[0]
    mac_ver_no = int(mac_ver.split('.')[1])
    if mac_ver_no < 9:
        print("Using lxml<2.4")
        lxml_requirement = "lxml<2.4"

setup(
    name="readability-lxml",
    version="0.6.3",
    author="Yuri Baburov",
    author_email="burchik@gmail.com",
    description="fast html to text parser (article readability tool) with python3 support",
    test_suite = "tests.test_article_only",
    long_description=open("README.rst").read(),
    license="Apache License 2.0",
    url="http://github.com/buriy/python-readability",
    packages=['readability', 'readability.compat'],
    install_requires=[
        "chardet",
        lxml_requirement,
        "cssselect"
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",

    ],
)
