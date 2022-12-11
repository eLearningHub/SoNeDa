"""Test cases for the __main__ module."""

from soneda.twitter.app import config
from soneda.twitter.client import TwitterAPIClient


def test_tweets_lookup() -> None:
    """Tweets lookup test."""
    config()
    twitter = TwitterAPIClient()
    tweet = twitter.get("/2/tweets", ids=1460323737035677698)
    print(tweet)
    assert tweet[0]["id"] == "1460323737035677698"
