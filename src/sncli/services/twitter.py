import click
import os

@click.group()
def twitter():
    pass

@twitter.command()
@click.option('--api-key', type=str, help='API key', default=lambda: os.environ.get("TWITTER_API_KEY", ""))
@click.option('--api-secret-key', type=str, help='API secret key', default=lambda: os.environ.get("TWITTER_API_SECRET_KEY", ""))
@click.option('--bearer-token', type=str, help='Bearer token', default=lambda: os.environ.get("TWITTER_BEARER_TOKEN", ""))
@click.option('--access-token', type=str, help='Access token', default=lambda: os.environ.get("TWITTER_ACCESS_TOKEN", ""))
@click.option('--access-token-secret', type=str, help='Access token secret', default=lambda: os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", ""))
def configure():
    click.echo('Configure the Twitter account')
