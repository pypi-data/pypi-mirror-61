#!/usr/bin/env python3
# This file is part of the Dataphile package.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Setup and installation script for Dataphile package."""

# standard libs
import os
from setuptools import setup, find_packages

# internal libs
from dataphile.__meta__ import (__appname__,
                                __version__,
                                __authors__,
                                __contact__,
                                __license__)


CMD_PREFIX = 'data.'  # Change this to '' to remove prefix on all commands
TOOLS = ['{prefix}{name}=dataphile{module}:main'.format(prefix=CMD_PREFIX, name=name, module=module)
         for name, module in {'phile':    '',  # TODO: 'main' application remains undecided
                              'stream':   '.bin.stream',
                              'groupby':  '.bin.groupby',
                              'compress': '.bin.compress',
                              # TODO: 'connect': '.bin.connect',
                              # TODO: 'watch':   '.bin.watch',
                              # TODO: 'monitor': '.bin.monitor',
                              # TODO: 'find':    '.bin.find',
                              # TODO: 'search':  '.bin.search',
                              # TODO: 'unique':  '.bin.unique',
                              # TODO: 'add':     '.bin.add',
                              # TODO: 'mean':    '.bin.mean',
                              # TODO: 'select':  '.bin.select',
                              # TODO: 'where':   '.bin.where',
                              # TODO: 'dropna':  '.bin.dropna',
                              }.items()]


def readme_file():
    """Use README.md as long_description."""
    with open(os.path.join(os.path.dirname(__file__), "README.md"), 'r') as readme:
        return readme.read()


setup(
    name             = __appname__,
    version          = __version__,
    author           = __authors__,
    author_email     = __contact__,
    description      = 'Data analytics library and command line data-ops tools.',
    license          = __license__,
    keywords         = 'data science tools analytics optimization',
    url              = 'https://dataphile.readthedocs.io',
    packages         = find_packages(),
    long_description = readme_file(),
    long_description_content_type = 'text/markdown',
    classifiers      = ['Development Status :: 4 - Beta',
                        'Topic :: Scientific/Engineering',
                        'Programming Language :: Python :: 3.5',
                        'Programming Language :: Python :: 3.6',
                        'Programming Language :: Python :: 3.7',
                        'License :: OSI Approved :: Apache Software License', ],
    install_requires = ['numpy', 'scipy', 'matplotlib', 'seaborn', 'pandas', 'astropy', 'tqdm',
                        'h5py', 'logalpha<2'],
    entry_points     = {'console_scripts': TOOLS},
)
