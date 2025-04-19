# tobot
Palindrome News Bot for [Bluesky](https://bsky.app/tobot)

Locally run utiltiy that matches current headlines with palindromes.  Will post skeets with palindromes and links to the news stories they match.  Human-curated to avoid mean-spirited posts.

## Setup

This repo is set up to use VENV.  Set up the folder by running `python -m venv ./`

Activate the venv by running one of the `activate` scripts in  `./Scripts`

Make a copy of the creds script and add your News API and Twitter creds.  Add your creds to the local environment variables by running `source creds_yourcredsscript.sh` or `CredsSettingFile.ps1`.  Be careful not to edit and then commit your creds.

Run the script with `python tobot.py`

## Creds

Credentials are accessed from Environment Variables.  Bash and pwsh examples are included to make setting these a breeze.  This script requires:

- News API Key

- Bluesky credentials (set up an App Password for this so you don't risk exposing your actual password)

## Palindromes

Files with one palindrome per line have been added to ./ext/

Palindromes are sourced from wikimedia, with permission from Twitter's [@pdromeprompt](https://twitter.com/pdromeprompt), and my own personal creations.  Add your own to a file and add the file to the `file_list` variable.  Add sourcing on every line in the palindrome file for it to appear in the tweet.

When tweets are used, they are added to a file that prevents their reuse for a configurable number of iterations.

## Matcher

The matcher:
- Tokenizes headlines and palindromes from its subscribed news services and palindrome list.
- Removes tokens for common words using a configurable number of words in the Google 10000 word list.
- Creates a tuple based on tokens in common between the headlines and palindromes
- Presents the list of matches to the user.

## Skeets

Skeets are limited to 299 characters total, palindrome + sourcing + news link.  Skeets are curated by the user instead of posting automatically.  Try not to be sardonic or punch down, please.
