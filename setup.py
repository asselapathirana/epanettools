#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
# import sys
import os
import re
from glob import glob
# from os.path import relpath
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

# from setuptools import find_packages
from setuptools import Extension
from setuptools import setup
from setuptools.command.test import test as TestCommand

# in windows use microsoft compilers
if os.name == 'nt':
 
    compilerargs = ['/DDLL#1', ]
    linkerargs   = []
else:
    compilerargs = ['-Wno-format','-O0'] 
    linkerargs   = []






# from setuptools.command.build_ext import build_ext
# from collections import defaultdict

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        tox.cmdline(args=args)


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


# Enable code coverage for C code: we can't use CFLAGS=-coverage in tox.ini, since that may mess with compiling
# dependencies (e.g. numpy). Therefore we set SETUPPY_CFLAGS=-coverage in tox.ini and copy it to CFLAGS here (after
# deps have been safely installed).
if 'TOXENV' in os.environ and 'SETUPPY_CFLAGS' in os.environ:
    os.environ['CFLAGS'] = os.environ['SETUPPY_CFLAGS']

sources = [
    "src" + os.sep + "epanettools" + os.sep + "epanet" + os.sep + x for x in ["epanet.c",
                                                                              "hash.c",
                                                                              "hydraul.c",
                                                                              "inpfile.c",
                                                                              "input1.c",
                                                                              "input2.c",
                                                                              "input3.c",
                                                                              "mempool.c",
                                                                              "output.c",
                                                                              "quality.c",
                                                                              "report.c",
                                                                              "rules.c",
                                                                              "smatrix.c"
                                                                              ]]
sources.append("src" + os.sep + "epanettools" + os.sep + "epanet2_wrap.c")

# 25-Aug-2016 - append emitter modification files
sources = sources + list(
    "src" + os.sep + "epanettools" + os.sep +
    "pdd" + os.sep + x for x in ["emitter_analysis.cpp",
                                 "mods.cpp", "wrap.cpp", ])
sources.append("src" + os.sep + "epanettools" + os.sep + "patch.c")
sources.append("src" + os.sep + "epanettools" + os.sep + "pdd_wrap.cxx")
# ^^^^^ NOTE: keep pdd_wrap.cxx as last element in sources
# - we remove that below using the fact that it is the last element
#  12-Nov-2016 - append adf calculation files

sources2 = sources[:-1] + list(
    "src" + os.sep + "epanettools" + os.sep + "adf" + os.sep + x for x in ["callepanet.cc",
                                                                           ])

sources2.append("src" + os.sep + "epanettools" + os.sep + "adf_wrap.cxx")





setup(
    name='EPANETTOOLS',
    version='1.0.0',
    license='GPLv3+',
    description='Epanet 2.0 Python calling interface',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub(
            '', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Assela Pathirana',
    author_email='assela@pathirana.net',
    url='https://github.com/asselapathirana/epanettools',
    packages=["epanettools"],
    include_dirs=[],
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+) ',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            'epanettools = epanettools.cli:main',
        ]
    },
    ext_modules=[
        Extension('_epanet2',
                  sources=sources,
                  extra_compile_args=compilerargs,
                  extra_link_args=linkerargs,
                  include_dirs=[
                      "src/epanettools/adf", "src/epanettools/epanet", "src/epanettools/pdd"]
                  ),
        Extension('_pdd',
                  sources=sources,
                  extra_compile_args=compilerargs,
                  extra_link_args=linkerargs,
                  include_dirs=[
                      "src/epanettools/adf", "src/epanettools/epanet", "src/epanettools/pdd"]
                  ),
        Extension('_adf',
                  sources=sources2,
                  extra_compile_args=compilerargs,
                  extra_link_args=linkerargs,
                  include_dirs=[
                      "src/epanettools/adf", "src/epanettools/epanet", "src/epanettools/pdd"]
                  )

    ],
    tests_require=['tox'],
)
