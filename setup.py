#!/usr/bin/env python

import os

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="django-rapyd-wiretap",
    version="0.0.4",
    description="Logs requests and responses to your application in a DB for auditing or troubleshooting purposes.",
    long_description=readme,
    author="Karthic Raghupathi",
    author_email="karthicr@gmail.com",
    url="https://github.com/karthicraghupathi/django_rapyd_wiretap_project",
    license=license,
    package_dir={"": "src"},
    packages=["wiretap", "wiretap.migrations"],
    install_requires=["django>=3,<3.3"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
