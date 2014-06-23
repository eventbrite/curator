from contextlib import contextmanager
import os

from invoke import (
    run,
    task,
)


@contextmanager
def base_directory():
    current_path = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    yield
    os.chdir(current_path)


@task
def test(failfast=False):
    with base_directory():
        command = 'python setup.py nosetests --with-coverage --cover-erase --cover-package=curator'
        if failfast:
            command += ' -x'
        run(command, pty=True)
