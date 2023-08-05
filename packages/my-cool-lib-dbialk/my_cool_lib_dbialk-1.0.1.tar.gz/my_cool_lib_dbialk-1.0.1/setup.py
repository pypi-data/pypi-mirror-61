#!/user/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='my_cool_lib_dbialk',
    version='1.0.1',
    author='Dawid Bialk',
    author_email='dev@example.com',
    url="https://github.com/",
    packages=find_packages(),
    include_package_data=True,
    description='Super useful library',
    install_requires=['names'],
    scripts=['get_names/gen_names_dbialk.py', 'bin/get_name_dbialk.bat']
)