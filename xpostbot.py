import praw
import config
import time
from datetime import datetime

import pprint

orig_sub = config.orig_sub
xpost_sub =  config.xpost_sub
max_time = config.max_time

def bot_login():
    r = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "A bot for crossposting deleted threads.")
    return r

def run(r):
    while True:
        scan_removed_posts(r)

        # Can add more functionality here as necessary

        print ("Exiting...")
        return
        #time.sleep(1800) # go through the log once every half hour

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

# TODO
# Check to see whether a post has already been crossposted
def is_present(title, post_id):
    return True

def post_time_out_of_range(log):
    if (time.time() - log.created_utc > max_time):
        print ("Thread too old")
        return True

r = bot_login()
run(r)
