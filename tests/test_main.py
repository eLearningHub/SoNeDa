"""Test cases for the __main__ module."""

import os

from soneda.twitter.client import TwitterAPIClient


def test_tweets_lookup() -> None:
    """Tweets lookup test."""
    twitter = TwitterAPIClient(
        os.getenv("TWITTER_PROFILE"),
        os.getenv("TWITTER_CONSUMER_KEY"),
        os.getenv("TWITTER_CONSUMER_SECRET"),
        os.getenv("TWITTER_ACCESS_TOKEN_KEY"),
        os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        os.getenv("TWITTER_BEARER_TOKEN"),
    )
    tweet = twitter.get("/2/tweets", ids=1460323737035677698)
    print(tweet)
    assert tweet[0]["id"] == "1460323737035677698"
