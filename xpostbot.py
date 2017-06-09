import praw
import config

def bot_login():
    r = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "test script for xpostbot")
    return r

def run(r):
    for log in r.subreddit('gringie_box').mod.log():
        print ("Mod: {}, Subreddit: {}".format(log.mod, log.subreddit))

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
