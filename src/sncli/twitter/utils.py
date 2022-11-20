import os
import toml

from sncli.twitter.exceptions import MissingCredentials

def twitter_credentials_file() -> str:
    return os.path.expanduser(os.getenv("TWITTER_CREDENTIALS_FILE", "~/.sncli/.twitter"))

def twitter_profiles() -> dict:
    dot_twitter = twitter_credentials_file()
    profiles = toml.load(dot_twitter)
    return profiles

def twitter_credentials(profile: str = None) -> dict:
    profiles = twitter_profiles()

    if profile is None:
      profile = list(profiles.keys())[0]
    
    return profiles[profile]
