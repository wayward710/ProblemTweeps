# Imports list of screen names from text files and blocks

import tweepy

consumer_key = 'YOUR_CONSUMER_KEY_HERE'
consumer_secret = 'YOUR_CONSUMER_SECRET_HERE'
access_token = 'YOUR_ACCESS_TOKEN_HERE'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET_HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# File containing list of screen names to block
blockfile = "junk/blocks.txt"

with open(blockfile) as in_file:
    for line in in_file:
        screenname = line.strip()
        try:
            print("trying to block ", screenname)
            api.create_block(screen_name=screenname)
        except:
            print("error in creating block ", screenname)
