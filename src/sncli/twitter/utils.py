import os
import toml
from requests_oauthlib import OAuth1Session

def get_twitter_credentials_file():
    return os.path.expanduser(os.getenv("TWITTER_CREDENTIALS_FILE", "~/.sncli/.twitter"))

def twitter_profiles():
    dot_twitter = get_twitter_credentials_file()
    profiles = toml.load(dot_twitter)
    return profiles

def twitter_api():
    profile = "default"
    profiles = twitter_profiles()
    consumer_key = os.environ.get("CONSUMER_KEY", profiles[profile]['consumer_key'])
    consumer_secret = os.environ.get("CONSUMER_SECRET", profiles[profile]['consumer_secret'])
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)

    # # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")
    
    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    
    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    
    response = oauth.get(
        "https://api.twitter.com/2/users/by", params=params
    )
    
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )
    
    print("Response code: {}".format(response.status_code))
    
    json_response = response.json()
    
    print(json.dumps(json_response, indent=4, sort_keys=True))