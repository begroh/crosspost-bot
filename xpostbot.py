import praw
import config

import pprint

orig_sub = ''
xpost_sub = ''

def bot_login():
    r = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "test script for xpostbot")
    return r

def run(r):
    for log in r.subreddit(orig_sub).mod.log(action='removelink'):
        link_id = log.target_fullname[3:]
        title = log.target_title
        body = log.target_body
        r.subreddit(xpost_sub).submit(title, body)

# TODO Finds new deletions in the mod log
def parse_mod_log():
    pass

# TODO 
def crosspost():
    pass

# TODO Finds mod comment with stated reason for removal
def get_removal_reason():
    pass

r = bot_login()
run(r)
