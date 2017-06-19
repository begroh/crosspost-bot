import os
import praw
from praw.models import MoreComments
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

# Only do posts from past [max_time]
def scan_removed_posts(r):
    posts_removed = []
    for log in r.subreddit(orig_sub).mod.log(action='removelink'):
        # Don't auto post AutoMod removals, wait for official mod removal
        if log._mod == 'AutoModerator':
            continue

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

        # In the case of a post being removed multiple times, ignore the 2nd
        if post_id in posts_removed:
            print ('Post "' + title + '" was already removed, skipping')
            continue

        posts_removed.append(post_id)
        submission_id = r.subreddit(xpost_sub).submit(title, selftext=body)

        removal_comment = get_removal_reason(r, post_id[3:])
        if removal_comment is not None:
            comment = r.submission(id=submission_id).reply(removal_comment)
            comment.mod.distinguish()

""" Crosspost helper functions """
# Finds mod comment with stated reason for removal
def get_removal_reason(r, post_id):
    submission = r.submission(id=post_id)
    submission.comment_sort = 'new' # Mod reason for removal should always be newest
    submission.comments.replace_more(limit=0)

    for top_level_comment in submission.comments:
        if top_level_comment.distinguished == 'moderator':
            return top_level_comment.body
    return None

def post_time_out_of_range(log):
    if (time.time() - log.created_utc > max_time):
        print ("Thread too old")
        return True
    return False

""" Functions to scan for deck winrates in the title and body """
def scan_title(r, title_string):
    pass

def scan_body(r, body_text):
    pass

r = bot_login()
run(r)
