import os

def get_twitter_credentials_file():
    return os.path.expanduser(os.getenv('TWITTER_CREDENTIALS_FILE', '~/.twitter/credentials'))
