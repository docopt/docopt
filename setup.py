"""`docopt` lives on `GitHub <http://github.com/halst/docopt/>`_."""
from setuptools import setup


setup(
    name = "docopt",
    version = "0.4.0",
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
        "License :: OSI Approved :: MIT License",
    ],
)
