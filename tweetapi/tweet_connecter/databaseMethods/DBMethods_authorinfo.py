import datetime
import pymongo
import tweepy
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
print(BASE_DIR)

import keys
import time

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

dblist = myclient.list_database_names()
mydb = myclient["tweeters_info"]
tweetersinfo = mydb["tweeters_info"]

consumer_key = keys.API_key
consumer_secret = keys.API_key_secret
access_token = keys.Access_token
access_token_secret = keys.Access_token_secret


client = tweepy . Client (bearer_token = keys.bearer_token)

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())



def get_authors_from_database():
    authorsList = []
    for i in tweetersinfo.find():
        authorsList.append(i)


    return authorsList


def get_author_by_id(id):
    tweeter = None
    try:
        myquery = {"screen_name":id}
        tweeter = tweetersinfo.find_one(myquery)

    except:
        print("author not found")

    return tweeter


