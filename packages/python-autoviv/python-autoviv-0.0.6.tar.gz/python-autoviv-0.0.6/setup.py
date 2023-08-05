import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


__version__ = '0.0.6'

setup(
    name='python-autoviv',
    version=__version__,
    description='Autovivification for Python',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/tysonholub/python-autoviv.git',
    author='Tyson Holub',
    author_email='tyson@tysonholub.com',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[]
)
