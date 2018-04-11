from os import path
from codecs import open
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='psynlp',
    version='1.0.4',
    description='A python module with Program Synthesis techniques for NLP',
    long_description=long_description,
    url='https://github.com/demfier/psynlp',

    author='Gaurav Sahu, Athitya Kumar',
    author_email='sahu.gaurav719@gmail.com',
    license='MIT',

    packages=find_packages(),

    install_requires=[
        'pandas',
        'networkx',
        'argparse'],

    keywords='nlp transducer program-synthesis oracle-learning ostia concept-lattice regex-learning pac-basis concept-learning'
    )
