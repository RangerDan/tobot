# tobot
Palindrome News Bot for Twitter

## Creds

Credentials are accessed from Environment Variables.  creds_example.sh is included to make setting these a breeze.  This script requires:

- News API Key

- Twitter Creds

## Palindromes

Files with one palindrome per line have been added to ./ext/

Palindromes are sourced from wikimedia, a collaboration with [@pdromeprompt](https://twitter.com/pdromeprompt), and my own personal stash.  Add your own to a file and add the file to the `file_list` variable.  Add sourcing on every line in the palindrome file for it to appear in the tweet.

When tweets are used, they are added to a file that prevents their reuse for a configurable number of iterations.

## Tweets

Tweets are limited to 280 characters total, palindrome + sourcing + news link.  Tweets are curated to not be sardonic or punch down.
