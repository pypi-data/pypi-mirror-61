#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    Copyright (C) 2019, Kai Raphahn <kai.raphahn@laburec.de>
#

from setuptools import setup, find_packages
import bbutil

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = find_packages(where=".", exclude=["tests", "tests.logging"])

setup(
    name=bbutil.__name__,
    license=bbutil.__license__,
    version=bbutil.__version__,
    description=bbutil.__description__,
    author=bbutil.__author__,
    author_email=bbutil.__email__,
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=[
        'run-tests.py',
    ],
    url='https://github.com/TheUncleKai/bbutils',
    packages=packages,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'colorama'
    ]
)
