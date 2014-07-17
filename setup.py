#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

lxml_requirement = "lxml"
if sys.platform == 'darwin':
    import platform
    mac_ver = platform.mac_ver()[0]
    if mac_ver < '10.9':
        print("Using lxml<2.4")
        lxml_requirement = "lxml<2.4"

setup(
    name="readability-lxml",
    version="0.3.0.3",
    author="Yuri Baburov",
    author_email="burchik@gmail.com",
    description="fast python port of arc90's readability tool",
    test_suite = "tests.test_article_only",
    long_description=open("README").read(),
    license="Apache License 2.0",
    url="http://github.com/buriy/python-readability",
    packages=['readability'],
    install_requires=[
        "chardet",
        lxml_requirement
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
)
