#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010-2017  IRISA
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# The original code contained here was initially developed by:
#
#     Pierre Vignet.
#     IRISA/IRSET
#     Dyliss team
#     IRISA Campus de Beaulieu
#     35042 RENNES Cedex, FRANCE

"""Definition of setup function for setuptools module."""

# Standard imports
import sys
from distutils import sysconfig
from setuptools import setup, Extension, find_packages
from setuptools.command.test import test as TestCommand

__PACKAGE_VERSION__ = "0.3"
__LIBRARY_VERSION__ = "1.1.0"

################################################################################

class PyTest(TestCommand):
    """Call tests with the custom 'python setup.py test' command."""

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

################################################################################

# Delete unwanted flags for C compilation
# Distutils has the lovely feature of providing all the same flags that
# Python was compiled with. The result is that adding extra flags is easy,
# but removing them is a total pain. Doing so involves subclassing the
# compiler class, catching the arguments and manually removing the offending
# flag from the argument list used by the compile function.
# That's the theory anyway, the docs are too poor to actually guide you
# through what you have to do to make that happen.
d = sysconfig.get_config_vars()
for k, v in d.items():
    for unwanted in (' -g ',):
        if str(v).find(unwanted) != -1:
            v = d[k] = str(v).replace(unwanted, ' ')

modules = [
    Extension(
        "_cadbiom",
        ["_cadbiom/cadbiom.c"],
        language = "c",
        include_dirs=['_cadbiom', '.'],
        define_macros=[
            ('CADBIOM_VERSION', '"' + __LIBRARY_VERSION__ + '"'),
        ],
        extra_compile_args=[
            "-flto",
            #"-march=native",
            #"-mtune=native",
            "-Ofast",
            #"-Wall",
            #"-g", # Not define NDEBUG macro => Debug build
            "-DNDEBUG", # Force release build
            "-std=c11",
            "-Wno-unused-variable",
            "-Wno-unused-but-set-variable",
            # assume that signed arithmetic overflow of addition, subtraction
            # and multiplication wraps around using twos-complement
            # representation
            "-fwrapv",
            # BOF protect (use both)
            #"-D_FORTIFY_SOURCE=2",
            #"-fstack-protector-strong",
            "-pthread",
            "-DUSE_PTHREADS",
        ],
        extra_link_args=[
            "-fPIC",
            "-Ofast",
            #"-march=native",
            "-flto",
            "-std=c11",
            "-Wl,--as-needed",
        ]
    ),
]

setup(
    name="cadbiom",
    version=__PACKAGE_VERSION__,
    author="Pierre Vignet",
    author_email="pierre.vignet@irisa.fr",
    url="https://gitlab.inria.fr/pvignet/cadbiom",

    # Search all packages recursively
    packages=find_packages(),

    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Natural Language :: French",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    ext_modules=modules,
    description="Cadbiom library v%s" % __LIBRARY_VERSION__,
    long_description=open('README.md').read(),
    install_requires=[
        "pip>=20.0",
        "networkx<2", "lxml",
        "pycryptosat>0.1.2", "antlr3-python-runtime==3.4",
        "cached-property>=1.5,<1.6",
    ],
    # TODO: use setup.cfg instead of these directives.
    # => Will allow to finely distinguish dev, and extra packages
    extras_require = {
        "dev": ["sphinx<2", "sphinx-argparse"], # For doc
    },

    # Tests
    tests_require=['pytest<3.7'],
    cmdclass={'test': PyTest},
)
