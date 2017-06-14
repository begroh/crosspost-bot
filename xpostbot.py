import os
import praw
import time
from datetime import datetime

import pprint

orig_sub = os.environ['ORIG_SUB']
xpost_sub =  os.environ['XPOST_SUB']
max_time = 600

def bot_login():
    r = praw.Reddit(username = os.environ['REDDIT_USERNAME'],
                    password = os.environ['REDDIT_PASSWORD'],
                    client_id = os.environ['REDDIT_ID'],
                    client_secret = os.environ['REDDIT_SECRET'],
                    user_agent = "A bot for crossposting deleted threads.")
    return r

def run(r):
    scan_removed_posts(r)

    # Can add more functionality here as necessary

# TODO Only do posts from past [time period]
def scan_removed_posts(r):
    for log in r.subreddit(orig_sub).mod.log(action='removelink'):
        post_id = log.target_fullname
        title = log.target_title
        body = log.target_body

        # Because of a praw bug, if the text body is None and the url is None
        # the submission will fail
        if body is None:
            body = ''

        # If post is older than the bot's time between checks you're done
        if post_time_out_of_range(log):
            break

        r.subreddit(xpost_sub).submit(title, selftext=body)
        # time.sleep(10) # Not sure if I need to wait between posts?

# TODO Finds mod comment with stated reason for removal
def get_removal_reason():
    pass

def post_time_out_of_range(log):
    if (time.time() - log.created_utc > max_time):
        print ("Thread too old")
        return True

r = bot_login()
run(r)
