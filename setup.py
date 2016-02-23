#!/usr/bin/env python 
"""
setup.py file for EPANET2 pyton library  - Assela Pathirana
"""
import os, sys
from setuptools import setup, Extension
from setuptools.command.test import test as TestCommand
	
import numpy 

from itertools import product

version = '0.5.0.8.dev0'

with open("README.txt","r") as f:
    README=f.read()
	

sources=[ "epanettools"+os.sep+"epanet"+os.sep+x for x in ["epanet.c",
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
sources.append("epanettools"+os.sep+"epanet2_wrap.c")
 
cargs=['-Wno-unused-but-set-variable','-Wno-format','-Wno-char-subscripts', '-fopenmp','-Wno-deprecated','-O3']
epanet2_module = Extension('_epanet2',
                           sources=sources,
                           extra_compile_args=cargs,
                           extra_link_args=cargs,
                           #extra_compile_args=['-O0', '-g', '-Wall']
                           )



EXAMPLES=["simple"]
EXTS=["inp", "py"]
EXTS.extend([x.upper() for x in EXTS])
EXAMPLES=list(product(EXAMPLES,EXTS))
package_data=[ "examples/"+x[0]+"/*."+x[1] for x in EXAMPLES]
NAME='EPANETTOOLS'
VERSION=version
SETUPNAME=NAME+"-"+version
LICENSE=u"GNU General Public License version 3"
LONGDISC="""Python interface for the popular water network model EPANET 2.0 engine. 
EPANET2 is realeased by United States Environmental Protection Agency to public domain. 
This python package is copyrighted by Assela Pathirana and released under %(lc)s. 

==========
README.txt
==========

%(rm)s

""" % {"lc": LICENSE, "rm": README}
CLASSIFY=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Environment :: Other Environment",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
        "Natural Language :: English"
        ]
		

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)		

setup (name = NAME,
       version = version,
       author      = "Assela Pathirana",
       author_email = "assela@pathirana.net",
       description = """EPANET 2.0  calls from python""",       
       packages = ["epanettools"],
	   ext_modules = [epanet2_module],
       include_dirs=[numpy.get_include()],
       package_data={'epanettools': package_data},
       license=LICENSE,
       url=u"http://assela.pathirana.net/EPANET-Python",
       long_description = LONGDISC, 
       classifiers=CLASSIFY,
	   tests_require=['pytest'],
	   cmdclass={'test': PyTest},
	   extras_require={
        'testing': ['pytest'],
    }
	   
       )
