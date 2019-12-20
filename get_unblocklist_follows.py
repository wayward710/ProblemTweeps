import time
import tweepy


# Credentials from Twitter developer account
consumer_key = 'YOUR_CONSUMER_KEY_HERE'
consumer_secret = 'YOUR_CONSUMER_SECRET_HERE'
access_token = 'YOUR_ACCESS_TOKEN_HERE'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET_HERE'

# Authn
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Get accounts that user_name follows
def get_follows(user_name):
    friends = []
    for page in tweepy.Cursor(api.friends, screen_name=user_name,
                              wait_on_rate_limit=True,
                              ait_on_rate_limit_notify=True, count=200).pages():
        try:
            friends.extend(page)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return friends


# Could set this up to take command-line args if wanted
if __name__ == '__main__':

    # Username you want follows for
    username = 'unblock_list'
    # File to save results to
    outfile = "D:/misc/junk/unblock_follows.txt"

    friend_vals = get_follows(username)
    str_found = str(len(friend_vals))

    # Sanity check -- how many IDS did we find?
    print(str_found, "ids found")

    # Generate tab-delimited text file with ID and screen name
    with open(outfile, 'w') as ofile:
        for friend in friend_vals:
            ofile.write(friend.id_str + '\t' + friend.screen_name + '\n')
