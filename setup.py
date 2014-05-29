import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

from docopt import __version__


class PyTestCommand(TestCommand):
    """ Command to run unit py.test unit tests
    """
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run(self):
        import pytest
        rcode = pytest.main(self.test_args)
        sys.exit(rcode)


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
    tests_require=[
            'pytest',
        ],
    cmdclass={
            'test': PyTestCommand,
        }
)
