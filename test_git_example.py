import ast
import os
import subprocess
import sys

from pytest import mark


ROOT = os.path.dirname(os.path.abspath(__file__))
EXAMPLES = os.path.join(ROOT, 'examples', 'git')


def run_git(arguments):
    env = os.environ.copy()
    env['PYTHONPATH'] = ROOT
    process = subprocess.Popen(
        [sys.executable, os.path.join(EXAMPLES, 'git.py')] + arguments,
        cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr


def help_text(filename):
    with open(os.path.join(EXAMPLES, filename)) as stream:
        return ast.get_docstring(ast.parse(stream.read()), clean=False).strip()


@mark.parametrize('arguments', [[], ['help'], ['--help'], ['-h']])
def test_git_global_help(arguments):
    status, stdout, stderr = run_git(arguments)
    assert status == 0
    assert stdout.strip() == help_text('git.py')
    assert not stderr


@mark.parametrize('command', [
    'add', 'branch', 'checkout', 'clone', 'commit', 'push', 'remote'])
def test_git_command_help(command):
    status, stdout, stderr = run_git(['help', command])
    assert status == 0
    assert stdout.strip() == help_text('git_%s.py' % command)
    assert not stderr


@mark.parametrize('arguments', [['unknown'], ['help', 'unknown']])
def test_git_unknown_command(arguments):
    status, stdout, stderr = run_git(arguments)
    assert status == 1
    assert "'unknown' is not a git.py command" in stderr
    assert 'Traceback' not in stderr


def test_git_version():
    status, stdout, stderr = run_git(['--version'])
    assert status == 0
    assert stdout.strip() == 'git version 1.7.4.4'
    assert not stderr


@mark.parametrize('arguments, expected', [
    (['add', 'example.txt'], "'<filepattern>': ['example.txt']"),
    (['branch', 'topic'], "'<branchname>': 'topic'"),
])
def test_git_normal_dispatch(arguments, expected):
    status, stdout, stderr = run_git(arguments)
    assert status == 0
    assert expected in stdout
    assert not stderr
