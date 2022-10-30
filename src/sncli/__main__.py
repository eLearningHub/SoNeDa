"""Command-line interface."""
from distutils.command.config import config
import click

@click.group()
def twitter():
    pass

@twitter.command()
def configure():
    click.echo('Configuring')

twitter.add_command(configure)

@click.command()
@click.version_option()
def main() -> None:
    """Social networks cli."""
    twitter()

if __name__ == "__main__":
    main(prog_name="sncli")  # pragma: no cover
