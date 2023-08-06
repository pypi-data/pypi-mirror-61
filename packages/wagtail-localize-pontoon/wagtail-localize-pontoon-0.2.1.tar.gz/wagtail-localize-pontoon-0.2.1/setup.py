#!/usr/bin/env python

import sys, os

from setuptools import setup, find_packages

# Hack to prevent "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when setup.py exits
# (see http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
except ImportError:
    pass


setup(
    name="wagtail-localize-pontoon",
    version="0.2.1",
    description="Pontoon integration for Wagtail Localize",
    author="Karl Hobley",
    author_email="karl@torchbox.com",
    url="",
    packages=find_packages(),
    include_package_data=True,
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        "wagtail_localize>=0.4,<0.5",
        "polib>=1.1,<2.0",
        "pygit2>=1.0,<2.0",
        "gitpython>=3.0,<4.0",
        "toml>=0.10,<0.11",
    ],
    extras_require={"testing": ["dj-database-url==0.5.0",],},
    zip_safe=False,
)
