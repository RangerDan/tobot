import os

class TobotCreds:
    creds = {}

    def __init__(self):
        self.creds['TWITTER_CONSUMER_KEY'] = os.environ['TWITTER_CONSUMER_KEY']
        self.creds['TWITTER_CONSUMER_SECRET'] = os.environ['TWITTER_CONSUMER_SECRET']
        self.creds['TWITTER_AUTH_TOKEN'] = os.environ['TWITTER_AUTH_TOKEN']
        self.creds['TWITTER_AUTH_SECRET'] = os.environ['TWITTER_AUTH_SECRET']
        self.creds['NEWS_API_KEY'] = os.environ['NEWS_API_KEY']

    def get_cred(self, cred_name):
        return self.creds[cred_name]
    