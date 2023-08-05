# -*- coding: utf-8 -*-


from setuptools import find_packages, setup

setup(
    name='get_names_strzelczyk',
    version='1.0.0',
    author='SomeCompany PLC',
    author_email='dave@example.com',
    packages=find_packages(),
    url="https://github.com",
    scripts=['gen_names_strzelczyk/gen_names_strzelczyk.py', 'bin/gen_names_strzelczyk.bat'],
    include_package_data=True,
    description='Super useful library',
    install_requires=['names']
)