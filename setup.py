import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "docopt",
    version = "0.1",
    author = "Vladimir Keleshev",
    author_email = "vladimir@keleshev.com",
    description = "Pythonic option parser, that will make you smile",
    license = "MIT",
    keywords = "option parsing optparse argparse getopt",
    url = "https://github.com/halst/docopt",
    py_modules=['docopt'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
