# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='jupyter-pip',
    version='0.3.1',
    description='Allows IPython notebook extension authors to make their extension pip installable!',
    author='Jonathan Frederic',
    author_email='jon.freder@gmail.com',
    license='New BSD License',
    url='https://github.com/jdfreder/jupyter-pip',
    keywords='python jupyter ipython javascript nbextension deployment pip install package extension',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python',
                 'License :: OSI Approved'],
    packages=['jupyterpip'],
    include_package_data=True,
)
