import logging
import click
import os

from sncli import logger
from sncli.functions.twitter import get_twitter_credentials_file



@click.group()
def twitter():
    pass


@twitter.command()
@click.option("--profile", type=str, help="Profile name", default=lambda: os.environ.get("TWITTER_PROFILE", "default"))
@click.option("--consumer-key", type=str, help="Access token", envvar="TWITTER_CONSUMER_KEY")
@click.option("--consumer-secret", type=str, help="Access token secret", envvar="TWITTER_CONSUMER_SECRET")
@click.option("--access-token-key", type=str, help="API key", envvar="TWITTER_ACCESS_TOKEN_KEY")
@click.option("--access-token-secret", type=str, help="API secret key", envvar="TWITTER_ACCESS_TOKEN_SECRET")
@click.option("--bearer-token", type=str, help="API secret key", envvar="TWITTER_BEARER_TOKEN")
@click.option("+overwrite/-overwrite", type=bool, help="Overwrite existing credentials")
def config(profile,consumer_key, consumer_secret, access_token_key, access_token_secret, bearer_token, overwrite):
    click.echo("Configuring a Twitter account")
    dot_twitter = get_twitter_credentials_file()
    if not os.path.exists(dot_twitter) or overwrite:
        os.system("mkdir -p ~/.sncli")
        f = open(dot_twitter, "wt")
        logger.info(f"Profile: {profile}")
        f.write(f"[{profile}]\n")
        f.write(f"consumer_key=\"{consumer_key}\"\n")
        f.write(f"consumer_secret=\"{consumer_secret}\"\n")
        f.write(f"access_token_key=\"{access_token_key}\"\n")
        f.write(f"access_token_secret=\"{access_token_secret}\"\n")
        f.write(f"bearer_token=\"{bearer_token}\"\n")
        f.close()

