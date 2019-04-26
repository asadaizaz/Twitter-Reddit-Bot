import tweepy
import requests
import praw
import os
import time
import pickle
from secrets import *

#ids = []
idfile = '/tmp/mydata.pk'
def twitterapi():
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def redditapi():
    reddit = praw.Reddit(client_id=REDDIT_C_KEY,
                         client_secret=REDDIT_C_SECRET,
                         password=REDDIT_SECRET,
                         user_agent='testscript by /u/fakebot3',
                         username=REDDIT_KEY)
    return reddit


def tweet_image(url, message):
    api = twitterapi()
    filename = '/tmp/temp.jpg'
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


url = "https://i.imgur.com/W8WbVCR.png"
message = "test"


def get_posts():
    reddit = redditapi()

    print(reddit.user.me())

    subreddit = reddit.subreddit('Kanye')

    ids = load_ids()
    top_python = subreddit.hot(limit=30)
    for submission in top_python:
        if not submission.stickied and not submission.selftext and submission.score > 500:
            if submission.id not in ids:
                print(submission.url)
                print(submission.title)
                ids.append(submission.id)
                tweet_image(submission.url, submission.title + '\n' + "#"' \n' + "redd.it/" + submission.id)
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


def lambda_handler(_even_json, _context):
    get_posts()
