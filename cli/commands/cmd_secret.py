import binascii
import os

import click


@click.command()
@click.argument('bytes', default=128)
def cli(bytes):
    """
    Generate a random secret token. Useful for generating a SECRET_KEY env
    variable suitable for production.

    :return: string
    """
    return click.echo(binascii.b2a_hex(os.urandom(bytes)))
