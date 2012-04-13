""" `docopt` lives on `GitHub <http://github.com/halst/docopt/>`_"""
from setuptools import setup


setup(
    name = "docopt",
    version = "0.1.1",
    author = "Vladimir Keleshev",
    author_email = "vladimir@keleshev.com",
    description = "Pythonic option parser, that will make you smile",
    license = "MIT",
    keywords = "option parsing optparse argparse getopt",
    url = "http://github.com/halst/docopt",
    py_modules=['docopt'],
    long_description=__doc__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
