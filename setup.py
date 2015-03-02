# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='ipython-pip',
    version='0.2',
    description='Allows IPython notebook extension authors to make their extension pip installable!',
    author='Jonathan Frederic',
    author_email='jon.freder@gmail.com',
    license='New BSD License',
    url='https://github.com/jdfreder/ipython-pip',
    keywords='python ipython javascript nbextension deployment pip install package extension',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python',
                 'License :: OSI Approved'],
    packages=['ipythonpip'],
    include_package_data=True,
)
