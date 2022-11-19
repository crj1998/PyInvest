from setuptools import setup, find_packages
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'requirements.txt'), 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='PyInvest',
    version='0.1',
    license='MIT',
    description='Python Investment tool',
    keywords='python invest strategy',
    author='meetslut',
    author_email='admin@meetslut.ml',
    url='https://github.com/nkaz001/hftbacktest',
    install_requires=requirements,
    packages=find_packages(),
)