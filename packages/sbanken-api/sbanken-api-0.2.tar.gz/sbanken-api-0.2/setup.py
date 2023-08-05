#!/usr/bin/env python3

from setuptools import setup

setup(
    name="sbanken-api",
    version="0.2",
    description="Easily communicate with Sbanken API in python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rolf Klausen",
    author_email="redacted@mail.com",
    url="https://github.com/abstrakct/sbanken-python",
    download_url="https://github.com/abstrakct/sbanken/archive/0.2.tar.gz",
    packages=["sbanken"],
    install_requires=[
        "certifi",
        "chardet",
        "idna",
        "oauthlib",
        "requests",
        "requests-oauthlib",
        "urllib3",
    ],
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
    ],
)
