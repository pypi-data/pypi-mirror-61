#!/usr/bin/env python
# setup.py

"""
Whisker setup file

To use:

    python setup.py sdist

    twine upload dist/*

To install in development mode:

    pip install -e .

"""
# https://packaging.python.org/en/latest/distributing/#working-in-development-mode  # noqa
# http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/
# http://jtushman.github.io/blog/2013/06/17/sharing-code-across-applications-with-python/  # noqa

import argparse
from setuptools import setup
import os
from os import path
import sys
from typing import List

from whisker.version import VERSION

# =============================================================================
# Constants
# =============================================================================

# Directories
THIS_DIR = path.abspath(path.dirname(__file__))

# Files
README_FILE = path.join(THIS_DIR, 'README.rst')  # read
PIP_REQ_FILE = os.path.join(THIS_DIR, 'requirements.txt')

# Arguments
EXTRAS_ARG = 'extras'

# Get the long description from the README file
with open(README_FILE, encoding='utf-8') as f:
    long_description = f.read()

SIMPLE_REQUIRES = [
    'arrow',  # better datetime
    'attrdict',  # dictionaries with attribute-style access
    'cardinal_pythonlib>=1.0.27',  # numpy doesn't install under RTD
    'colorama',  # colour at the command line
    'colorlog',  # colourful logs
    'dataset',  # databases for lazy people (used by demo)
    'Twisted',  # TCP/IP communications
    # 'typing==3.5.2.2',  # part of stdlib in Python 3.5, but not 3.4
    'pyyaml',  # Yet Another Markup Language
    'sqlalchemy',  # Databases
]

REQUIRES_THAT_RTD_DISLIKES = [
    'PyQt5',  # Qt for Python; needs C compiler; doesn't install on RTD
]  # see also fixes for Sphinx/autodoc in conf.py

DEVELOPMENT_ONLY_REQUIRES = [
    # ---------------------------------------------------------------------
    # For development only:
    # ---------------------------------------------------------------------
    'sphinx',  # for documentation
    'sphinx_rtd_theme',  # for documentation
    'twine',  # for uploading to PyPI
]

ON_READTHEDOCS = os.environ.get('READTHEDOCS') == 'True'

REQUIREMENTS = SIMPLE_REQUIRES
if not ON_READTHEDOCS:
    REQUIREMENTS += REQUIRES_THAT_RTD_DISLIKES


# =============================================================================
# Perform special actions if we're building a package
# =============================================================================

parser = argparse.ArgumentParser()
parser.add_argument(
    '--' + EXTRAS_ARG, action='store_true',
    help=(
        "USE THIS TO CREATE PACKAGES (e.g. 'python setup.py sdist --{}. "
        "Copies extra info in.".format(EXTRAS_ARG)
    )
)
our_args, leftover_args = parser.parse_known_args()
sys.argv[1:] = leftover_args

extra_files = []  # type: List[str]

if getattr(our_args, EXTRAS_ARG):
    # -------------------------------------------------------------------------
    # Write requirements.txt
    # -------------------------------------------------------------------------
    with open(PIP_REQ_FILE, "w") as req_file:
        req_file.writelines([
            "# This is an AUTOCREATED file, requirements.txt; see "
            "setup.py and DO NOT EDIT BY HAND"])
        req_file.write("\n\n" + "\n".join(REQUIREMENTS) + "\n")


# =============================================================================
# setup args
# =============================================================================

setup(
    name='whisker',

    version=VERSION,

    description='Whisker Python client library',
    long_description=long_description,

    # The project's main homepage.
    url='http://www.whiskercontrol.com/',

    # Author details
    author='Rudolf Cardinal',
    author_email='rudolf@pobox.com',

    # Choose your license
    license='Apache License 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        'Natural Language :: English',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3 :: Only',

        'Topic :: System :: Hardware',
        'Topic :: System :: Networking',
    ],

    keywords='whisker research control',

    packages=['whisker'],

    install_requires=REQUIREMENTS,

    entry_points={
        'console_scripts': [
            # Format is 'script=module:function".
            'whisker_test_rawsockets=whisker.test_rawsockets:main',
            'whisker_test_twisted=whisker.test_twisted:main',
        ],
    },
)
