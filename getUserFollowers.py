# Gets follower information for a list of users.  Identifies some likely
# to be TERF account.  Approach might work with a variety of abusive
# profiles -- e.g., white supremacists, etc
# Can be pulled into a spreadsheet program and sorted

import time
import tweepy
import csv
import re

# Credentials from Twitter developer account
consumer_key = 'YOUR_CONSUMER_KEY_HERE'
consumer_secret = 'YOUR_CONSUMER_SECRET_HERE'
access_token = 'YOUR_ACCESS_TOKEN_HERE'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET_HERE'

# Authn
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# return list of followers (no duplicates) corresponding to user IDs
def get_followers(users):
    api = tweepy.API(auth)
    followers = []
    for user_name in users:
        for page in tweepy.Cursor(api.followers, screen_name=user_name,
                                  wait_on_rate_limit=True,
                                  ait_on_rate_limit_notify=True, count=200).pages():
            try:
                followers.extend(x for x in page if x not in followers)
            except tweepy.TweepError as e:
                print("Going to sleep:", e)
                time.sleep(60)
    return followers


# save the list of followers to tab-delimited text file
# outfile -- name/location of file to save to
# data -- list of user objects
# -blocklist='blocktogetherfile' file containing blocklist ids
# -skip_blocklist=True/False (whether to include users on blocklist in output)

def save_followers_to_csv(outfile, data, **kwargs):

    blocklistids = []
    skip_blocklist = False

    if "blocklist" in kwargs.keys():
        with open(kwargs["blocklist"]) as blockfile:
            blocklines = blockfile.readlines();
            for bline in blocklines:
                blocklistids.append(int(bline.strip()))

    if "skipblocked" in kwargs.keys():
        skip_blocklist = kwargs["skipblocked"]

    # Stuff that frequently shows up in TERF profiles but not elsewhere
    terf_words = ['deboosted', 'gender critical', 'gendercritical',
                  'genderfree', 'human female', 'germaine greer',
                  'magdalen', 'terven', ' gc ', ', gc,', ',gc,',
                  'radfem', 'detrans', 'terfisaslur',
                  'spinster.xyz', 'meghan murphy',
                  'radical feminist', 'freemeghan',
                  'expense of women', 'shadow-banned',
                  'shadowbanned', 'shadow-banned',
                  'shadow banned', 'lgballiance',
                  'terf ', ' terf', ',terf', 'terf,', 'lgb ',
                  '\\ud83d\\udd78', '\\ud83d\\udd77',
                  'not the fun kind', 'gender abolitionist', 'the xx kind']

    # Twitter fields
    HEADERS = ["screen_name", "name", "description", "url", "followers_count",
               "friends_count", "location", "verified", "created_at"]
    # Add header item for TERF predictor
    HEADERS2 = ["screen_name", "name", "description", "url", "followers_count",
                "friends_count", "location", "verified", "created_at",
                "likely_terf", "onblocklist"]

    with open(outfile, 'w', encoding="utf-8", newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='\t')
        csv_writer.writerow(HEADERS2)
        for profile_data in data:
            profile = []
            # Look for TERFishness
            found_TERF = False
            string_to_compare = str(profile_data).lower()
            for term in terf_words:
                if term in string_to_compare:
                    found_TERF = True

            for header in HEADERS:
                profile.append(profile_data._json[header])
            profile.append(found_TERF)

            # Check to see if profile is in blocklist
            in_blocklist = False
            if profile_data.id in blocklistids:
                in_blocklist = True
            profile.append(in_blocklist)

            # Clean the newlines out of the description
            profile[2] = re.sub('\r?\n', ' ', profile[2])
            if not (in_blocklist and skip_blocklist):
                csv_writer.writerow(profile)


if __name__ == '__main__':
    problem_children = ["problemchild1", "problemchild2"]
    followers = get_followers(problem_children)
    save_followers_to_csv("junk/garbage.txt", followers,
                          blocklist="junk/TTurfer-blocklist2.csv", skipblocked=True)
