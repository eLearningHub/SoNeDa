import os
import typer
from typing import Optional

from sncli.cli import console
from sncli.functions.twitter import get_twitter_credentials_file

twitter_app = typer.Typer()

@twitter_app.command()
def config(profile: Optional(str) = typer.Argument("default", envvar="TWITTER_PROFILE", help="Profile name"),
           consumer_key: Optional(str) = typer.Argument(None, envvar="TWITTER_CONSUMER_KEY", help="Access token"),
           consumer_secret: Optional(str) = typer.Argument(None, envvar="TWITTER_CONSUMER_SECRET", help="Access token secret"),
           access_token_key: Optional(str) = typer.Argument(None, envvar="TWITTER_ACCESS_TOKEN_KEY", help="API key"),
           access_token_secret: Optional(str) = typer.Argument(None, envvar="TWITTER_ACCESS_TOKEN_SECRET", help="API secret key"),
           bearer_token: Optional(str) = typer.Argument(None, envvar="TWITTER_BEARER_TOKEN", help="bearer token"),
           overwrite: bool = typer.Option(True, "--overwrite/--append", help="Overwrite existing credentials")):
    console.print("Configuring a Twitter account")
    dot_twitter = get_twitter_credentials_file()
    if not os.path.exists(dot_twitter) or overwrite:
        os.system("mkdir -p ~/.sncli")
        f = open(dot_twitter, "wt")
        f.write(f"[{profile}]\n")
        f.write(f"consumer_key=\"{consumer_key}\"\n")
        f.write(f"consumer_secret=\"{consumer_secret}\"\n")
        f.write(f"access_token_key=\"{access_token_key}\"\n")
        f.write(f"access_token_secret=\"{access_token_secret}\"\n")
        f.write(f"bearer_token=\"{bearer_token}\"\n")
        f.close()
