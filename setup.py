"""`docopt` lives on `GitHub <http://github.com/halst/docopt/>`_."""
from setuptools import setup


setup(
    name = "docopt",
    version = "0.5.0",
    author = "Vladimir Keleshev",
    author_email = "vladimir@keleshev.com",
    description = "Pythonic argument parser, that will make you smile",
    license = "MIT",
    keywords = "option arguments parsing optparse argparse getopt",
    url = "http://docopt.org",
    py_modules=['docopt'],
    long_description=__doc__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "License :: OSI Approved :: MIT License",
    ],
)
