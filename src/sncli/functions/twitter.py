import os
import toml

def get_twitter_credentials_file():
    return os.path.expanduser(os.getenv("TWITTER_CREDENTIALS_FILE", "~/.sncli/.twitter"))

def twitter_profiles():
    dot_twitter = get_twitter_credentials_file()
    profiles = toml.load(dot_twitter)
    return profiles
