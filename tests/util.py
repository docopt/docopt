"""Utility helpers for Docopt tests."""

from docopt import docopt


def run_docopt(doc, argv='', **kwargs):
    """Helper to run ``docopt`` with given argv string."""
    if isinstance(argv, str):
        argv = argv.split() if argv else []
    return docopt(doc, argv=argv, **kwargs)
