#!/usr/bin/env python
import sys

from setuptools import setup

setup(
    name="readability-lxml",
    version="0.3.0.6",
    author="Yuri Baburov",
    author_email="burchik@gmail.com",
    description="fast python port of arc90's readability tool",
    test_suite="tests.test_article_only",
    long_description=open("README").read(),
    license="Apache License 2.0",
    url="http://github.com/buriy/python-readability",
    packages=['readability'],
    install_requires=[
        "chardet",
        "lxml",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
