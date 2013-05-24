#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="readability-lxml",
    version="0.2.6.2",
    author="Miguel Galves",
    author_email="mgalves@gmail.com",
    description="fast python port of arc90's readability tool",
    test_suite = "tests.test_article_only",
    long_description=open("README").read(),
    license="Apache License 2.0",
    url="http://github.com/mgalves/python-readability",
    packages=['readability'],
    install_requires=[
        "chardet",
        "lxml"
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
)
