from atproto import Client, models
from newsapi import NewsApiClient
import re
import string
from creds import TobotCreds
import requests
import unicodedata

TOP_10000_WORDS_FILE = 'ext/google-10000-english-usa-no-swears.txt'
RECENTLY_USED_PALINDROMES_FILE = 'ext/recently-used-palindromes.txt'
PALINDROME_FILES = ['ext/palindromes.txt','ext/dans-novel-palindromes.txt','ext/palindrome-prompts.txt']
NEWS_SOURCES = ['abc-news','al-jazeera-english','ars-technica','associated-press','axios',
                'bbc-news','bloomberg','buzzfeed',
                'cbc-news','cbs-news','cnn','engadget','financial-post','fortune',
                'google-news','ign','independent','mtv-news','newsweek',
                'reuters','techcrunch','techradar','the-washington-post','wired']

class Palindrome:
    def __init__(self, text):
        self.text = text
        self.keywords = set(re.sub('['+string.punctuation+']', '', text.lower()).split())

    def remove_blocked_keywords(self, blocked_words: set):
        # Patches a list of relevant keywords to each Palindrome using text
        # and removes blocked words.
        self.keywords = self.keywords - blocked_words

    def is_palindrome(self):
        # Normalize the text by removing spaces and converting to lowercase
        split_text = self.text.split('@')[0].split('#')[0].lower()
        normalized_text = unicodedata.normalize('NFKD', split_text)
        ascii_text = ''.join([c for c in normalized_text if not unicodedata.combining(c)])
        no_punctuation = ''.join(e for e in ascii_text if e.isalnum())
        return no_punctuation == no_punctuation[::-1]
    
    def __repr__(self):
        return f"Palindrome({self.text})"
    
    def __str__(self):
        return f"Palindrome: {self.text}"

class Article:
    def __init__(self, source_name, title, description, url, urlToImage, content):
        self.source_name = source_name
        self.title = title
        self.description = description
        self.url = url
        self.urlToImage = urlToImage
        self.content = content

        all_text = ((self.title or "empty")+ " " + (self.description or "empty")).lower()
        self.keywords = set(re.sub('['+string.punctuation+']', '', all_text).split())
    
    def remove_blocked_keywords(self, blocked_words: set):
        # Patches a list of relevant keywords to each Article using title and description
        # and removes blocked words.
        self.keywords = self.keywords - blocked_words

    def __repr__(self):
        return f"Article({self.title})"
    
    def __str__(self):
        return f"Article: {self.title}\nSource: {self.source_name}\nURL: {self.url}"

class Pair:
    def __init__(self, palindrome: Palindrome, article: Article):
        self.palindrome = palindrome
        self.article = article

    def __repr__(self):
        return f"Pair({self.palindrome}, {self.article})"

    def __str__(self):
        return f"Pair: {self.palindrome} with {self.article}"

def get_articles(api_key):
    """
    Returns a list of articles from the News API.
    The articles are filtered to only include those from the specified sources.
    The articles are in English.
    The function returns None if there is an error.

    Articles are returned in the following format:
    [
        {
            'source': {'id': 'abc-news', 'name': 'ABC News'},
            'author': 'John Doe',
            'title': 'Breaking News: Something Happened',
            'description': 'A description of the news article.',
            'url': 'https://example.com/news/article',
            'urlToImage': 'https://example.com/image.jpg',
            'publishedAt': '2023-10-01T12:00:00Z',
            'content': 'The content of the news article.'
        },
        ...
    ]
    """
    
    newsapi = NewsApiClient(api_key)
        
    try:
        articles = []
        response = newsapi.get_top_headlines(
            sources=','.join(NEWS_SOURCES),
            language='en')
        for article in response['articles']:
            articles.append(Article(article['source']['name'],
                                    article['title'],
                                    article['description'],
                                    article['url'],
                                    article['urlToImage'],
                                    article['content']))
        return articles
    except Exception as e:
        print("Error: {}".format(e))
        return None

def get_blocked_wordlist():
    # Reduces matching noise on 'a' 'an' etc.
    blocked_wordlist = []
    infile = open(TOP_10000_WORDS_FILE,'r')
    for line in infile:
        blocked_wordlist.append(line.strip())
    infile.close()
    return set(blocked_wordlist[0:300])

def recently_used_palindromes(set_blocked_wordlist):
    # List last 20 recently used palindromes
    # TODO Make the file reading a function
    recently_used_list = []
    infile = open(RECENTLY_USED_PALINDROMES_FILE, 'r', encoding='utf-8')
    for line in infile:
        candidate = Palindrome(line.strip())
        if (candidate.is_palindrome()):
            candidate.remove_blocked_keywords(set_blocked_wordlist)
            recently_used_list.append(candidate)
        else:
            print("Not a palindrome: {}".format(candidate.text))
    infile.close()
    return recently_used_list

def collect_all_palindromes(recent: list, set_blocked_wordlist: set):
# Make Palindrome list (ignoring recently-used palindromes)
    palindromes = []
    for palindrome_file in PALINDROME_FILES:
        infile = open(palindrome_file, 'r', encoding='utf-8')
        for line in infile:
            candidate = Palindrome(line.strip())
            if candidate.is_palindrome():
                candidate.remove_blocked_keywords(set_blocked_wordlist)
                palindromes.append(candidate)
            else:
                print("Not a palindrome: {}".format(candidate.text))
        infile.close()
    return list(set(palindromes) - set(recent[-200:]))

def find_pairs(articles, palindromes):
    # Pair up articles with palindromes
    pairs = []
    for article in articles:
        for palindrome in palindromes:
            if article.keywords & palindrome.keywords:
                pairs.append(Pair(palindrome, article))
    return pairs

def print_pairs(pairs):
# Print all pairs of articles and palindromes
    for index, pair in enumerate(pairs, start=1):
        if (len(pair.palindrome.text) + 24 + 12 <= 280):
            print("Pair {}:".format(index))
            print(" P - {}".format(pair.palindrome))
            print(" A - {}".format(pair.article))
        else:
            print("SKIPPED {}".format(index))

def post_it(pairs, bluesky_username, bluesky_password):
    # Choose a palindrome from the list by user input and consider posting it to Twitter
    choice_char = input("Which one should I post (integer)?") 
    if not choice_char.isnumeric() or int(choice_char) < 1 or int(choice_char) > len(pairs):
        return
    
    choice = int(choice_char) - 1

    # Create a Bluesky client
    client = Client("https://bsky.social")
    client.login(bluesky_username, bluesky_password)

    # Create the tweet
    response = requests.get(pairs[choice].article.urlToImage, stream=True)
    response.raise_for_status()  # Raise an exception for bad status codes

    # Upload the blob using the atproto client
    upload = client.upload_blob(response.content)

    link_card = models.AppBskyEmbedExternal.External(
        uri=pairs[choice].article.url,
        title=pairs[choice].article.title,
        description=pairs[choice].article.description,
        thumb=upload.blob,
    )
    
    embed = models.AppBskyEmbedExternal.Main(external=link_card)
    post_text = pairs[choice].palindrome.text + " #palindrome"

    print("Posting the following text:")
    print(post_text)
    print(embed)
    if input("Should I post this?") == 'y':
        client.send_post(text=post_text, embed=embed)
        
        # Add to end of "recently-posted" list
        infile = open(RECENTLY_USED_PALINDROMES_FILE,'a')
        infile.write('\n')
        infile.write(pairs[choice].palindrome.text)
        infile.close()

def main():
    creds = TobotCreds()
    blocked_words = get_blocked_wordlist()
    top_articles = get_articles(creds.get_cred('NEWS_API_KEY'))
    for article in top_articles:
        article.remove_blocked_keywords(blocked_words)
    print("Found {} articles.".format(len(top_articles)))
    blocked_palindromes = recently_used_palindromes(blocked_words)
    palindromes = collect_all_palindromes(blocked_palindromes, blocked_words)
    print("Found {} palindromes.".format(len(palindromes)))
    pairs = find_pairs(top_articles, palindromes)
    print_pairs(pairs)
    post_it(pairs, creds.get_cred("BLUESKY_USERNAME"), creds.get_cred("BLUESKY_PASSWORD"))

if __name__ == "__main__":
    main()