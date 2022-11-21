import os
import re
import base64
import hashlib
import oauthlib
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2.rfc6749.errors import MissingTokenError

from sncli.twitter.utils import twitter_credentials
from sncli.twitter.exceptions import MissingToken

class TwitterAPIClient:

    API_ROOT = os.environ.get("TWITTER_API_ROOT", "https://api.twitter.com")
    AUTH_URL = "https://twitter.com/i/oauth2/authorize"
    TOKEN_URL = f"{API_ROOT}/2/oauth2/token"
    REDIRECT_URI = "http://127.0.0.1:5000/oauth/callback"

    def __init__(self, profile: str = None):
        self.scops = ["tweet.read", "users.read", "tweet.write", "offline.access"]

        credentials = twitter_credentials(profile)
        self.consumer_key = credentials['consumer_key']

        # Create a code verifier
        self.code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
        self.code_verifier = re.sub("[^a-zA-Z0-9]+", "", self.code_verifier)

        # Create a code challenge
        code_challenge = hashlib.sha256(self.code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
        self.code_challenge = code_challenge.replace("=", "")

        self.client = OAuth2Session(self.client_id, redirect_uri=self.REDIRECT_URI, scope=self.scopes)

    def fernet(self, key: str) -> Fernet:
        key = key + "=" * (len(key) % 4)
        _key = base64.urlsafe_b64encode(base64.urlsafe_b64decode(key))
        return Fernet(_key)

    def encrypt(self, data: str) -> bytes:
        return self.fernet(self.app_secret).encrypt(data.encode())

    def decrypt(self, data: bytes) -> bytes:
        return self.fernet(self.app_secret).decrypt(data)

    def token_saver(self, token: dict) -> None:
        logger.debug("SAVING TOKEN: %s" % str(token))
        data = json.dumps(token)
        _t = self.encrypt(data)
        with dbm.open(KEY_DB.as_posix(), "c") as db:
            db[self.app_id] = _t

    def load_saved_token(self) -> dict:
        with dbm.open(KEY_DB.as_posix(), "c") as db:
            _token = db[self.app_id]
        token = json.loads(self.decrypt(_token))
        return token

    def fetch_api_token(self) -> dict:
        backend = BackendApplicationClient(client_id=self.app_id)
        oauth = OAuth2Session(client=backend)
        try:
            token = oauth.fetch_token(
                token_url=self.TOKEN_URL,
                client_id=self.app_id,
                client_secret=self.app_secret,
                include_client_id=True,
            )
        except MissingTokenError:
            # oauthlib gives the same error regardless of the problem
            print("Something went wrong, please check your client credentials.")
            raise
        return token

    def clear_saved_token(self) -> None:
        with dbm.open(KEY_DB.as_posix(), "c") as db:
            if self.app_id in db:
                del db[self.app_id]

    def reset(self):
        self.clear_saved_token()
        token = self.fetch_api_token()
        self.token_saver(token)
        self.client = self.create_client_for_token(token)

    ### Dispatch methods ###

    def get(self, path:str, **query) -> requests.Response:
        url = f"{self.TWITTER_API_ROOT}{path}"
        if query:
            querystr = urllib.parse.urlencode(query)
            url = f"{url}?{querystr}"
        logger.debug(f"GETing URL {url}")
        try:
            return self.client.get(url)
        except (oauthlib.oauth2.rfc6749.errors.MissingTokenError, MissingToken):
            self.reset()
            return self.client.get(url)

    def post(self, path:str, data:dict) -> requests.Response:
        url = self.api_url+path
        #logger.debug(f"POSTing URL {url}")
        headers={
            "Authorization": "Bearer {}".format(token["access_token"]),
            "Content-Type": "application/json",
        }
        return self.client.post(url, json=data, headers=headers)

    def put(self, path:str, data:dict) -> requests.Response:
        url = f"{self.TWITTER_API_ROOT}{path}"
        logger.debug(f"PUTing URL {url}")
        try:
            resp = self.client.put(url, json=data)
            return resp
        except (oauthlib.oauth2.rfc6749.errors.MissingTokenError, MissingToken):
            self.reset()
            resp = self.client.post(url, json=data)
            return resp
