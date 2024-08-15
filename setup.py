#!/usr/bin/env python

import codecs
import os
import re
from setuptools import setup
import sys

lxml_requirement = "lxml"
if sys.platform == "darwin":
    import platform

    mac_ver = platform.mac_ver()[0]
    mac_major, mac_minor = mac_ver.split('.')[:2]
    if int(mac_major) == 10 and int(mac_minor) < 9:
        print("Using lxml<2.4")
        lxml_requirement = "lxml<2.4"

speed_deps = [
     "cchardet",
]

def _get_html_clean_deps():
    if lxml_requirement != "lxml":
        return []
    if sys.version_info <= (3, 11):
        return ["lxml", "lxml_html_clean"]
    return ["lxml[html_clean]"]


html_clean_deps = _get_html_clean_deps()

test_deps = [
    # Test timeouts
    "wrapt-timeout-decorator",
] + html_clean_deps

extras = {
    'speed': speed_deps,
    'test': test_deps,
    'html_clean': html_clean_deps
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
    long_description=open("README.rst").read(),
    long_description_content_type='text/x-rst',
    license="Apache License 2.0",
    url="http://github.com/buriy/python-readability",
    packages=["readability"],
    install_requires=["chardet", lxml_requirement, "cssselect"],
    tests_require=test_deps,
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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
)
