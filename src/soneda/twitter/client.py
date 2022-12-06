"""TwitterAPIClient."""

import base64
import dbm
import hashlib
import json
import os
import re
import urllib
import json
from typing import Any
from typing import Dict
from typing import Optional

import requests
import toml
from cryptography.fernet import Fernet
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2.rfc6749.errors import MissingTokenError
from requests_oauthlib import OAuth2Session  # type: ignore


CREDENTIALS_FILE = os.path.expanduser(
    os.getenv("TWITTER_CREDENTIALS_FILE", "~/.soneda/.twitter")
)


class TwitterAPIClient:
    """TwitterAPIClient.

    Attributes:
        get: REST API GET
        post: REST API POST
        put: REST API PUT
    
    Example:
        >>> twitter = TwitterAPIClient()
        >>> tweet = twitter.get("/2/tweets", ids=1460323737035677698)
        >>> assert tweet[0]["id"] == "1460323737035677698"
    """

    API_ROOT = os.environ.get("TWITTER_API_ROOT", "https://api.twitter.com")
    AUTH_URL = "https://twitter.com/i/oauth2/authorize"
    REFRESH_URL = f"{API_ROOT}/oauth2/token-refresh"
    TOKEN_URL = f"{API_ROOT}/oauth2/token"
    REDIRECT_URI = "http://127.0.0.1:5000/oauth/callback"
    API_ROOT = os.environ.get("TWITTER_API_ROOT", "https://api.twitter.com")
    KEY_DB = os.path.expanduser(os.getenv("TWITTER_KEY_DB", "~/.soneda/.twitter.key"))
    scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]

    def __init__(self, profile: Optional[str] = None):
        """Initialize Twitter client with token."""
        profiles = toml.load(CREDENTIALS_FILE)
        if profile is None:
            profile = list(profiles.keys())[0]

        credentials = profiles[profile]
        self.consumer_key = credentials["consumer_key"]
        self.consumer_secret = credentials["consumer_secret"]

        # Create a code verifier
        self.code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
        self.code_verifier = re.sub("[^a-zA-Z0-9]+", "", self.code_verifier)

        # Create a code challenge
        code_challenge = hashlib.sha256(self.code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge)
        self.code_challenge = code_challenge.decode("utf-8").replace("=", "")

        if os.path.exists(self.KEY_DB):
            token = self.load_saved_token()
        else:
            token = self.fetch_api_token()
            self.token_saver(token)

        self.client = self.create_client_for_token(token)

    def fernet(self, key: str) -> Fernet:
        """fernet."""
        _key = bytes(key[0:32], "utf-8")
        _key = base64.urlsafe_b64encode(_key)
        return Fernet(_key)

    def encrypt(self, data: str) -> bytes:
        """encrypt."""
        return self.fernet(self.consumer_secret).encrypt(data.encode())

    def decrypt(self, data: bytes) -> bytes:
        """decrypt."""
        return self.fernet(self.consumer_secret).decrypt(data)

    def token_saver(self, token: Dict[str, str]) -> None:
        """Saves the token in a local database."""
        data = json.dumps(token)
        _t = self.encrypt(data)
        with dbm.open(self.KEY_DB, "c") as db:
            db[self.consumer_key] = _t

    def load_saved_token(self) -> Any:
        """Loads the token from a local database."""
        try:
            with dbm.open(self.KEY_DB, "c") as db:
                _token = db[self.consumer_key]
            token = json.loads(self.decrypt(_token))
            return token
        except MissingTokenError as e:
            raise KeyError from e

    def fetch_api_token(self) -> Any:
        """Fetches the API token."""
        backend = BackendApplicationClient(client_id=self.consumer_key)
        oauth = OAuth2Session(client=backend)
        try:
            token = oauth.fetch_token(
                token_url=self.TOKEN_URL,
                client_id=self.consumer_key,
                client_secret=self.consumer_secret,
            )
        except MissingTokenError:
            # oauthlib gives the same error regardless of the problem
            print("Something went wrong, please check your client credentials.")
            raise
        return token

    def create_client_for_token(self, token: Dict[str, str]) -> OAuth2Session:
        """Creates a client for a given token."""
        backend = BackendApplicationClient(client_id=self.consumer_key)
        return OAuth2Session(
            client=backend,
            scope=self.scopes,
            token=token,
            auto_refresh_url=self.REFRESH_URL,
            auto_refresh_kwargs={},
            token_updater=self.token_saver,
        )

    def clear_saved_token(self) -> None:
        """Removes the saved token from a local database."""
        with dbm.open(self.KEY_DB.as_posix(), "c") as db:
            if self.consumer_key in db:
                del db[self.consumer_key]

    def reset(self) -> None:
        """Renews the token and creates a new client."""
        self.clear_saved_token()
        token = self.fetch_api_token()
        self.token_saver(token)
        self.client = self.create_client_for_token(token)

    # Dispatch methods

    def get(self, path: str, **query: Any) -> Dict[str, Any]:
        """REST API GET method."""
        url = f"{self.API_ROOT}{path}"
        if query:
            querystr = urllib.parse.urlencode(query)
            url = f"{url}?{querystr}"
        # logger.debug(f"GETing URL {url}")
        try:
            response = self.client.get(url)
        except MissingTokenError:
            self.reset()
            response = self.client.get(url)
        
        return  response.json()["data"]

    def post(self, path: str, data: Dict[str, str]) -> requests.Response:
        """REST API POST method."""
        url = f"{self.API_ROOT}{path}"
        # logger.debug(f"POSTing URL {url}")
        return self.client.post(url, json=data)

    def put(self, path: str, data: Dict[str, str]) -> requests.Response:
        """REST API PUT method."""
        url = f"{self.API_ROOT}{path}"
        # logger.debug(f"PUTing URL {url}")
        try:
            resp = self.client.put(url, json=data)
            return resp
        except MissingTokenError:
            self.reset()
            resp = self.client.post(url, json=data)
            return resp
