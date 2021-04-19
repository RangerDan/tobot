import tweepy
from newsapi import NewsApiClient
import json
import re
import string
import pprint
import random
from creds import TobotCreds

creds = TobotCreds()

# Get news stories
newsapi = NewsApiClient(api_key = creds.get_cred('NEWS_API_KEY'))
top_articles = newsapi.get_top_headlines(
    sources='abc-news,al-jazeera-english,ars-technica,associated-press,bbc-news,cbc-news,cbs-news,google-news,newsweek,reuters,the-washington-post',
    language='en')['articles']

# Get blocked word list to reduce matching noise on 'a' 'an' etc.
blocked_wordlist = []
infile = open('ext/google-10000-english-usa-no-swears.txt','r')
for line in infile:
    blocked_wordlist.append(line.strip())
infile.close()
set_blocked_wordlist = set(blocked_wordlist[0:300])

# Pair Article URLs with possible keywords among article headlines (ignoring blocked words)
article_keyword_tuples = []
for article in top_articles:
    content_text = ((article['title'] or "empty")+ " " + (article['description'] or "empty")).lower()
    possible_content_keywords = set(re.sub('['+string.punctuation+']', '', content_text).split())
    keywords = possible_content_keywords - set_blocked_wordlist
    keywords_with_article = (article['url'], keywords)
    article_keyword_tuples.append(keywords_with_article)

# List last 20 recently used palindromes
recently_used_list = []
infile = open('ext/recently-used-palindromes.txt','r')
for line in infile:
    recently_used_list.append(line.strip())
infile.close()

# Make Palindrome list (ignoring recently-used palindromes)
palindrome_list = []
file_list = ['ext/palindromes.txt','ext/dans-novel-palindromes.txt','ext/palindrome-prompts.txt']
for palindrome_file in file_list:
    infile = open(palindrome_file,'r')
    for line in infile:
        if line.strip() not in recently_used_list[-200:]:
            palindrome_list.append(line.strip())
    infile.close()

# Create list of palindrome keywords (removing blocked words)
palindrome_keyword_tuples = []
for palindrome in palindrome_list:
    palindrome_text = palindrome.lower()
    possible_palindrome_keywords = set(re.sub('['+string.punctuation+']', '', palindrome_text).split())
    palindrome_keywords = possible_palindrome_keywords - set_blocked_wordlist
    if palindrome_keywords:
        palindrome_with_palindrome_keywords = (palindrome,palindrome_keywords)
        palindrome_keyword_tuples.append(palindrome_with_palindrome_keywords)

# Pair up articles with palindromes
palindrome_article_pairs = []
for article in article_keyword_tuples:
    for palindrome in palindrome_keyword_tuples:
        if article[1] & palindrome[1]:
            found_pair = (palindrome,article)
            palindrome_article_pairs.append(found_pair)

# Print all pairs of articles and palindromes
for index, pair in enumerate(palindrome_article_pairs, start=1):
    if (len(pair[0][0]) + 24 + 12 <= 280):
        print("{}:".format(index))
        print("- {}".format(pair[0][0]))
        print("-- {}".format(pair[1][0]))
    else:
        print("SKIPPED {}".format(index))

# Choose a palindrome from the list by user input and consider posting it to Twitter
choice = input("Which one should I post (integer)?") 
if choice.isnumeric() and int(choice) >= 1 and int(choice) <= len(palindrome_article_pairs):
    
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(creds.get_cred('TWITTER_CONSUMER_KEY'), creds.get_cred('TWITTER_CONSUMER_SECRET'))
    auth.set_access_token(creds.get_cred('TWITTER_AUTH_TOKEN'), creds.get_cred('TWITTER_AUTH_SECRET'))

    # Create API object
    api = tweepy.API(auth)
    
    # Create the tweet
    selection_formated = palindrome_article_pairs[int(choice)-1][0][0] + " #palindrome " + palindrome_article_pairs[int(choice)-1][1][0]
    print (selection_formated)

    if input("Should I post this?") == 'y':
        api.update_status(selection_formated)
        # Add to end of "recently-posted" list
        infile = open('ext/recently-used-palindromes.txt','a')
        infile.write('\n')
        infile.write(palindrome_article_pairs[int(choice)-1][0][0])
        infile.close()
