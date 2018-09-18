#!/usr/bin/python3
# Kenny Jarnagin, Hanover College Fall 2018

# Accessing the Twitter API
# This script describes the basic methodology for accessing a Twitter feed
# or something similar.

# Loading libraries needed for authentication and requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import json
import operator

# In order to use this script, you must:
# - Have a Twitter account and create an app
# - Store in keys.json a property called "twitter" whose value is an
#     object with two keys, "key" and "secret"
with open('keys.json', 'r') as f:
   keys = json.loads(f.read())['twitter']

twitter_key = keys['key']
twitter_secret = keys['secret']

# We authenticate ourselves with the above credentials
# We will demystify this process later
#
# For documentation, see http://requests-oauthlib.readthedocs.io/en/latest/api.html
# and http://docs.python-requests.org/en/master/
client = BackendApplicationClient(client_id=twitter_key)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='https://api.twitter.com/oauth2/token',
                          client_id=twitter_key,
                          client_secret=twitter_secret)

# Base url needed for all subsequent queries
base_url = 'https://api.twitter.com/1.1/'

# Particular page requested. The specific query string will be
# appended to that.
page = 'search/tweets.json'

# Depending on the query we are interested in, we append the necessary string
# As you read through the twitter API, you'll find more possibilities
req_url = base_url + page + '?q=Hanover+College&tweet_mode=extended&count=100'

# We perform a request. Contains standard HTTP information
response = oauth.get(req_url)

# Read the query results
results = json.loads(response.content.decode('utf-8'))

## Process the results
## CAUTION: The following code will attempt to read up to 10000 tweets that
## Mention Hanover College. You should NOT change this code.
tweets = results['statuses']
while True:
   if not ('next_results' in results['search_metadata']):
      break
   if len(tweets) > 10000:
      break
   next_search = base_url + page + results['search_metadata']['next_results'] + '&tweet_mode=extended'
   print(results['search_metadata']['next_results'])
   response = oauth.get(next_search)
   results = json.loads(response.content.decode('utf-8'))
   tweets.extend(results['statuses'])

## CAUTION: For the rest of this assignment, the list "tweets" contains all the
## tweets you would want to work with. Do NOT change the list or the value of "tweets".

text_list = [text['full_text'] for text in tweets]


#if the provided tweet was retweeted, get the full text of that retweet
#otherwise, just return the full text of the given tweet
def get_full_text(tweet):
  if "retweeted_status" in tweet:
    return tweet['retweeted_status']['full_text'];
  else:
    return tweet['full_text'];

text_list_full = [get_full_text(tweet) for tweet in tweets]

#Return a list of hashtags from a given tweet
def hashtagParser(tweet):
  counter = len(tweet['entities']['hashtags'])
  hashtags = []
  while counter > 0:
    i = 0
    hashtags.append(tweet['entities']['hashtags'][i]['text'])
    i+=1
    counter-=1
  return hashtags;

tags_per_tweet = [hashtagParser(tweet) for tweet in tweets]

#Create a hashtags dictionary counting the number of repeated hashtags in the given tweets
hashtags = {}
for tags in tags_per_tweet:
  for hashtag in tags:
    if hashtag in hashtags:
      hashtags[hashtag]+=1
    else:
      hashtags[hashtag] = 1

sorted_hashtags = sorted(hashtags.items(), key=operator.itemgetter(1), reverse=True)
#Grab the top six hashtags from the given tweets
top_six_hashtags = []
for i in range (0,6):
  top_six_hashtags.append(sorted_hashtags[i])

