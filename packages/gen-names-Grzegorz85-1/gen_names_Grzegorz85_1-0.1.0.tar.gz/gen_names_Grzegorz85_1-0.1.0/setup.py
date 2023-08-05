# -*- config: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name ='gen_names_Grzegorz85_1',
    version='0.1.0',
    author ='SomeComapany',
    author_email='dev@example.com',
    packages = find_packages(),
    include_package_data=True,
    description ='Super useful library',
    scripts=['gen_names_Grzegorz85/gen_names_Grzegorz85.py','bin/gen_names_Grzegorz85.bat'],
    install_requires=['names']
)
