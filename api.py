import io, json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# Binds gmaps_key to the contents of google_secret.txt as a string
gmaps_key = open('google_secret.txt').read()

# Opens 'yelp_secret.json' with variable name cred
with io.open('yelp_secret.json') as cred:

    # Converts file-object "cred" into Python dictionary and assigns to "creds"
    creds = json.load(cred)

    # Instantiates Oauth1Authenticator object with API keys in "creds"
    auth = Oauth1Authenticator(**creds)

    # Constructs Client object using Oauth1Authenticator object
    yelp_client = Client(auth)