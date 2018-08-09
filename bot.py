import tweepy
import requests
import praw
import os
import time
import pickle
from secrets import *


idfile = 'mydata.pk'
subredditname = 'Kanye'
def twitterapi():
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def redditapi():
    reddit = praw.Reddit(client_id=REDDIT_C_KEY,
                         client_secret=REDDIT_C_SECRET,
                         password=REDDIT_SECRET,
                         user_agent='twitter bot /u/',
                         username=REDDIT_KEY)
    return reddit


def tweet_image(url, message):
    api = twitterapi()
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        if not os.path.getsize(filename) > 3072000:
         api.update_with_media(filename, status=message)
         os.remove(filename)
        else:
            print("Image to large!")
    else:
        print("Unable to download image")



def get_posts():
    reddit = redditapi()

    print(reddit.user.me())

    subreddit = reddit.subreddit(subredditname)

    ids = load_ids()
    top_python = subreddit.hot(limit=30)
    for submission in top_python:
        if not submission.stickied and not submission.selftext and submission.score > 500:
            print(submission.url)
            print(submission.title)
            if submission.id not in ids:
                ids.append(submission.id)
                tweet_image(submission.url, submission.title + '\n' + '\n' + "redd.it/" + submission.id)
                break
            else:
                print("Next submission")
                continue

    save_ids(ids)
    print("Posted!")


def load_ids():
    ids = []
    if os.path.exists(idfile):
     with open(idfile, 'rb') as fi:
        ids = pickle.load(fi)

    return ids



def save_ids(ids) :
    with open(idfile, 'wb') as fi:
        pickle.dump(ids, fi)


