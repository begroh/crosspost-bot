import praw
import config
import time
from datetime import datetime

import sqlite3

import pprint

orig_sub = config.orig_sub
xpost_sub =  config.xpost_sub
max_time = config.max_time

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
        conn = sqlite3.connect('xposttest.db')
        c = conn.cursor()

        for log in r.subreddit(orig_sub).mod.log(action='removelink'):
            post_id = log.target_fullname
            title = log.target_title
            body = log.target_body
            
            # If the post is older than a specified amount of time, ignore it
            # Also means you're done
            if post_time_out_of_range(log):
                break

            # If the item has already been checked, we've gone through
            # all the new log entries
            if is_present(conn, c, post_id):
                break

            add_to_db(conn, c, post_id, title)

            # r.subreddit(xpost_sub).submit(title, body)
            #time.sleep(60) # Don't want it spamming so only do this once a minute

        conn.close()
        print ("Exiting...")
        return
        #time.sleep(3600) # go through the log once every hour

# TODO Finds mod comment with stated reason for removal
def get_removal_reason():
    pass

# Check to see whether a post is in the database
def is_present(conn, c, post_id):
    c.execute("SELECT * FROM seen WHERE id=?", (post_id,))
    if c.fetchone() is not None:
        print ("Thread has already been processed")
        return True
    print ("Thread not in database")
    return False

# Add a new post to the DB
def add_to_db(conn, c, post_id, title):
    try:
        c.execute("INSERT INTO seen (id, title) VALUES (?, ?)", (post_id, title))
        conn.commit()
        print ("Adding thread", title, "to database")
    except sqlite3.Error as e:
        print ("An error occured:", e.args[0])

    c.execute("SELECT * FROM seen")
    print (c.fetchall())

def post_time_out_of_range(log):
    if (time.time() - log.created_utc > max_time):
        print ("Thread too old")
        return True

r = bot_login()
run(r)
