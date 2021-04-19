# tobot
Palindrome News Bot for Twitter

Matches headlines with palindromes.  Will post tweets with palindromes and links to the news stories they match. 

## Setup

This repo is set up to use VENV.  Set up the folder by running `python -m venv ./`

Activate the venv with `source bin/activate`

Make a copy of the creds script and add your News API and Twitter creds.  Add your creds to the local environment variables by running `source creds_yourcredsscript.sh`.  Be careful not to edit and then commit your creds.

Run the script with `python tobot.py`

## Creds

Credentials are accessed from Environment Variables.  creds_example.sh is included to make setting these a breeze.  This script requires:

- News API Key

- Twitter Creds

## Palindromes

Files with one palindrome per line have been added to ./ext/

Palindromes are sourced from wikimedia, a collaboration with [@pdromeprompt](https://twitter.com/pdromeprompt), and my own personal stash.  Add your own to a file and add the file to the `file_list` variable.  Add sourcing on every line in the palindrome file for it to appear in the tweet.

When tweets are used, they are added to a file that prevents their reuse for a configurable number of iterations.

## Matcher

The matcher:
- Tokenizes headlines and palindromes from its subscribed news services and palindrome list.
- Removes tokens for common words using a configurable number of words in the Google 10000 word list.
- Creates a tuple based on tokens in common between the headlines and palindromes
- Presents the list of matches to the user.

## Tweets

Tweets are limited to 280 characters total, palindrome + sourcing + news link.  Tweets are curated by the user.  Try not to be sardonic or punch down, please.  You're not Noam Chomsky.
