import os

class TobotCreds:
    creds = {}

    def __init__(self):
        self.creds['BLUESKY_USERNAME'] = os.environ['BLUESKY_USERNAME']
        self.creds['BLUESKY_PASSWORD'] = os.environ['BLUESKY_PASSWORD']
        self.creds['NEWS_API_KEY'] = os.environ['NEWS_API_KEY']

    def get_cred(self, cred_name):
        return self.creds[cred_name]
    