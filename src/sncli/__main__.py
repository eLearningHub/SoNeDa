import sys
import logging
import click
from sncli.services.twitter import twitter

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@click.group()
def cli():
    pass

cli.add_command(twitter)

if __name__ == '__main__':
    cli()
