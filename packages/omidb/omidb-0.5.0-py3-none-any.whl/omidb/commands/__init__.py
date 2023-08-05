import click
from . import summarise


@click.group()
def entry_point():
    pass


def main():
    entry_point.add_command(summarise.cli)
    entry_point()
