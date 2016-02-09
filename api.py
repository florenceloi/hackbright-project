import io, json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

with io.open('yelp_secret.json') as cred:

    # Loads in yelp_secret.json
    creds = json.load(cred)

    # Instantiates Oauth1Authenticator object with API keys
    auth = Oauth1Authenticator(**creds)

    # Constructs client object using Oauth1Authenticator object
    client = Client(auth)