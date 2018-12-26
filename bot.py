from datetime import datetime
from itertools import repeat
from multiprocessing.pool import Pool

import praw
import os

from sentiment import get_comment_sentiment


whitelist = ['2meirl4meirl', 'absolutelynotme_irl', 'depression']
last_polled = {subreddit: datetime(year=2000, month=1, day=1).timestamp() for subreddit in whitelist}

USERNAME = os.environ['REDDIT_USER'] # TODO externalize to config file
PASSWORD = os.environ['REDDIT_PW']
CLIENT_ID = os.environ['REDDIT_ID']
CLIENT_SECRET = os.environ['REDDIT_SECRET']
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"


def init():
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=PASSWORD,
        user_agent=USER_AGENT,
        username=USERNAME)


def construct_message():
    return ('A TITLE', 'Hey..') # TODO


def process_submissions(reddit, subreddit):
    pass


def process_comments(reddit, subreddit):

    for comment in reddit.subreddit(subreddit).stream.comments():
        if comment.created_utc <= last_polled[subreddit]:
            break
        sentiment = get_comment_sentiment(comment)
        if (sentiment > 8): # TODO
            title, message = construct_message()
            print(f'Bot sending pm for comment: {comment.permalink(fast=False)}')
            reddit.redditor(comment.author).message(title, message) # TODO investigate the exception handling here


if __name__ == '__main__':
    # TODO -> should be able to multiprocess this with a new reddit process per subreddit.
    #       However, since they are all keyed from the same reddit account, we need to delegate the rate limiting
    #       between the instances (ie: a RedditHandler class)
    # with Pool() as pool:
    #     pool.starmap(process_comments, zip(repeat(init), whitelist))
    reddit = init()
    for subreddit in whitelist:
        process_comments(reddit, subreddit)
