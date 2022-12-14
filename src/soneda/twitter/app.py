"""Typer app commands."""
from typing import Optional

import typer

from soneda.cli import console
from soneda.twitter.client import TwitterAPIClient


twitter_app = typer.Typer()


@twitter_app.command()
def config(
    profile: Optional[str] = typer.Argument(
        "default", envvar="TWITTER_PROFILE", help="Profile name"
    ),
    consumer_key: Optional[str] = typer.Argument(
        None, envvar="TWITTER_CONSUMER_KEY", help="Access token"
    ),
    consumer_secret: Optional[str] = typer.Argument(
        None, envvar="TWITTER_CONSUMER_SECRET", help="Access token secret"
    ),
    access_token_key: Optional[str] = typer.Argument(
        None, envvar="TWITTER_ACCESS_TOKEN_KEY", help="API key"
    ),
    access_token_secret: Optional[str] = typer.Argument(
        None, envvar="TWITTER_ACCESS_TOKEN_SECRET", help="API secret key"
    ),
    bearer_token: Optional[str] = typer.Argument(
        None, envvar="TWITTER_BEARER_TOKEN", help="bearer token"
    ),
    overwrite: bool = typer.Option(
        True, "--overwrite/--append", help="Overwrite existing credentials"
    ),
) -> None:
    """Configure a Twitter profile."""
    console.print("Configuring a Twitter account")
    TwitterAPIClient(
        profile,
        consumer_key,
        consumer_secret,
        access_token_key,
        access_token_secret,
        bearer_token,
        overwrite,
    )


@twitter_app.command()
def tweets(
    profile: Optional[str] = typer.Option(
        None, envvar="TWITTER_PROFILE", help="Profile name"
    ),
    ids: Optional[str] = typer.Argument(
        1460323737035677698, help="Required. Enter a single Tweet ID."
    ),
) -> None:
    """Tweets lookup."""
    twitter = TwitterAPIClient(profile)
    tweet = twitter.get("/2/tweets", ids=ids)
    print(tweet)
