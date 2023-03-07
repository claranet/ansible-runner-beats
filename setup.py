#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="ansible-runner-beats",
    version="1.0.3",
    author="Claranet",
    url="https://github.com/claranet/ansible-runner-beats",
    license="MPL2",
    packages=find_packages(),
    install_requires=required,
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"ansible_runner.plugins": "beats = ansible_runner_beats"},
    zip_safe=False,
)
