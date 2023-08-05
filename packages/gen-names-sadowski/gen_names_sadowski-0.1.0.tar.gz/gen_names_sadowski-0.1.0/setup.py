# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


setup(
    name='gen_names_sadowski',
    version='0.1.0',
    description='Generate random names with length',
    long_description='Generate random names with length',
    url='https://github.com/krzs13',
    author='Krzysztof Sadowski',
    author_email='krzysztofsadowski1989@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    keywords='random names',
    scripts=['gen_names_sadowski/gen_names_sadowski.py', 'bin/gen_names_sadowski.bat'],
    install_requires=['names'],
)

