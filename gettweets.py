import tweepy
import json
import re
import string
import pprint
import random
from creds import TobotCreds

creds = TobotCreds()

# Authenticate to Twitter
auth = tweepy.OAuthHandler(creds.get_cred('TWITTER_CONSUMER_KEY'), creds.get_cred('TWITTER_CONSUMER_SECRET'))
auth.set_access_token(creds.get_cred('TWITTER_AUTH_TOKEN'), creds.get_cred('TWITTER_AUTH_SECRET'))

# Create API object
api = tweepy.API(auth)

tweets = []
for status in tweepy.Cursor(api.user_timeline, id="pdromeprompt").items():
    if status.in_reply_to_status_id is None:
        tweets.append(status.text)
        tweets.append(str(status.created_at)) 

# Add to end of "recently-posted" list
infile = open('ext/pdromeprompt-raw.txt','a')
for tweet in tweets:
    infile.write(tweet)
    infile.write('\n------------------------------------------\n')
infile.close()
