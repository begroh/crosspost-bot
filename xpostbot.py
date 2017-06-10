import praw
import config
from time import sleep

import sqlite3

import pprint

orig_sub = config.orig_sub
xpost_sub =  config.xpost_sub

def bot_login():
    r = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "test script for xpostbot")
    return r

# TODO Only do posts from past [time period]
def run(r):
    while True:
        for log in r.subreddit(orig_sub).mod.log(action='removelink'):
            post_id = log.target_fullname
            title = log.target_title
            body = log.target_body

            # If the item has already been checked, we've gone through
            # all the new log entries
            if is_present(post_id, title):
                break

            pprint.pprint(vars(log))

            add_to_db(post_id, title)

            # r.subreddit(xpost_sub).submit(title, body)
            #sleep(60) # Don't want it spamming so only do this once a minute

        sleep(3600) # go through the log once every hour

# TODO Finds mod comment with stated reason for removal
def get_removal_reason():
    pass

# TODO
def add_to_db(post_id, title):
    pass

def is_present(post_id, title):
    pass

r = bot_login()
run(r)
