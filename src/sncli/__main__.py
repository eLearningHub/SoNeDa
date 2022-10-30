import click
from .services.twitter import twitter


@click.group()
def cli():
    pass

cli.add_command(twitter)
