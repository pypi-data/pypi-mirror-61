# See LICENSE file for details
"""Console script for repomanager."""

import click

from repomanager.rpm import rpm
from repomanager.__init__ import __version__

@click.command()
@click.version_option(version=__version__)
@click.option('--verbose', '-v', default='error', help='Set verbose level')
@click.option('--dir', '-d', default='', type=click.Path(), help='Work directory path')
@click.option('--clean','-c', is_flag='True', help='Clean builds')
@click.option('--repolist', default='repolist.yaml', type=click.File('r'), help='Repo list to be cloned')
@click.option('--update', '-u', is_flag='True', help='Update Repo for specified branch')
@click.option('--patch', '-p', 'apply', flag_value='patch', help='Apply patch to the repo')
@click.option('--unpatch', '-r', 'apply', flag_value='unpatch', help='Remove patch from the repo')
def cli(verbose, dir, clean, repolist, update, apply):
    rpm(verbose, dir, clean, repolist, update, apply)

if __name__ == '__main__':
    cli()
