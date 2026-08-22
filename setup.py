#!/usr/bin/env python

import codecs
import os
import re
from setuptools import setup

speed_deps = [
     "cchardet",
]

extras = {
    'speed': speed_deps,
}

# Adapted from https://github.com/pypa/pip/blob/master/setup.py
def find_version(*file_paths):
    here = os.path.abspath(os.path.dirname(__file__))

    # Intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *file_paths), "r") as fp:
        version_file = fp.read()
        version_match = re.search(
            r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M,
        )
        if version_match:
            return version_match.group(1)

    raise RuntimeError("Unable to find version string.")


setup(
    name="readability-lxml",
    version=find_version("readability", "__init__.py"),
    author="Yuri Baburov",
    author_email="burchik@gmail.com",
    description="fast html to text parser (article readability tool) with python 3 support",
    test_suite="tests.test_article_only",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    url="http://github.com/buriy/python-readability",
    packages=["readability"],
    python_requires=">=3.8.2,<3.15",
    install_requires=[
        "chardet",
        "lxml[html_clean]>=5.4,<7",
        "lxml-html-clean; python_version < '3.11'",
        "cssselect"
    ],
    extras_require=extras,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
