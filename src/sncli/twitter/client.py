import requests
from requests_oauthlib import OAuth2Session

class TwitterAPIClient:

    def __init__(self):
        self.auth_url = "https://twitter.com/i/oauth2/authorize"
        self.token_url = "https://api.twitter.com/2/oauth2/token"
        self.redirect_uri = "https://localhost/"
        self.scops = ["tweet.read", "users.read", "tweet.write", "offline.access"]

        # Create a code verifier
        self.code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
        self.code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

        # Create a code challenge
        code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
        code_challenge = code_challenge.replace("=", "")

        try:
            token = self.load_saved_token()
        except KeyError:
            token = self.fetch_api_token()
            self.token_saver(token)
        self.client = self.create_client_for_token(token)

    def create_client_for_token(self, token: dict) -> OAuth2Session:
        return OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scopes)

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
        url = f"{self.TWITTER_API_ROOT}{path}"
        logger.debug(f"POSTing URL {url}")
        try:
            resp = self.client.post(url, json=data)
            return resp
        except (oauthlib.oauth2.rfc6749.errors.MissingTokenError, MissingToken):
            self.reset()
            resp = self.client.post(url, json=data)
            return resp

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
