# -*- coding: utf -8 -*-

from setuptools import find_packages, setup


setup(
    name = 'namesss',
    version = '0.1.0',
    author= 'SomeCompanyPLC',
    packages = find_packages(),
    include_package_data= True,
    descripction= 'Super userfull library',
    url= 'https://github.com/joenkert/names',
    install_requires=['names'],
    keywords='random names',
    scripts=['gen_names_bozydar/gen_names_bozydae.py','bin/gen names.bat']

)