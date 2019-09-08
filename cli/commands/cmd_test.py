import subprocess
import os

import click


@click.command()
@click.argument('path', default=os.path.join('app', 'tests'))
def cli(path):
    """
    Run tests with Pytest. Will test "app/tests/" by default

    :param path: Test path
    :return: Subprocess call result
    """
    cmd = 'py.test {0}'.format(path)
    return subprocess.call(cmd, shell=True)
