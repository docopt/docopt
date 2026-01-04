from pathlib import Path
from setuptools import setup

from docopt import __version__

# Read the README file
readme_file = Path(__file__).parent / 'README.rst'
long_description = readme_file.read_text(encoding='utf-8')

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
    long_description=long_description,
    long_description_content_type='text/x-rst',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
)
