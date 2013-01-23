from setuptools import setup

from docopt import __version__


setup(
    name='docopt',
    version=__version__,
    author='Vladimir Keleshev',
    author_email='vladimir@keleshev.com',
    description='Pythonic argument parser, that will make you smile',
    license='MIT',
    keywords='option arguments parsing optparse argparse getopt',
    url='http://docopt.org',
    py_modules=['docopt'],
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'License :: OSI Approved :: MIT License',
    ],
)
