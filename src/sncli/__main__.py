import sys
import logging
import click
from .services.twitter import twitter

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('SNCLI')

@click.group()
def cli():
    pass

cli.add_command(twitter)

if __name__ == '__main__':
    cli()
