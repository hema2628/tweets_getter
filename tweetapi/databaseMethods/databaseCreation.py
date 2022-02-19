import datetime

import pymongo
import tweepy
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import authors
import keys
import time

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

dblist = myclient.list_database_names()
mydb = myclient["tweets"]
mytweetsinfo = mydb["tweets_info"]

consumer_key = keys.API_key
consumer_secret = keys.API_key_secret
access_token = keys.Access_token
access_token_secret = keys.Access_token_secret


client = tweepy . Client (bearer_token = keys.bearer_token)

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

def get_authors():
    author_enum= authors.Authors
    author_list = []
    for i in author_enum:
        author_list.append(i.value)
    return author_list

def insert_one(authorname,info):
    mydb = myclient["tweets"]

    target_Col = mydb[authorname]

    target_Col.insert_one(info)

def insert_many(authorname,infolist):
    mydb = myclient["tweets"]

    target_Col = mydb[authorname]

    target_Col.insert_many(infolist)

def tweet_getter_by_Id(id):
    public_tweets = api.user_timeline(screen_name=id)
    json_list = []
    for tweet in public_tweets:
        json_list.append(tweet)

    return json_list

def insert_new(authorname):
    target_col = mydb[authorname]
    res = target_col.find({},{ "_id": 0,"id":1})
    # get tweets id that already exist in the database
    tweets_id_list = []
    for i in res:
        tweets_id_list.append(str(i["id"]))

    # get new timeline and see whether each tweets is already in thedatabase
    # put the new tweet in the database
    new_tweets = tweet_getter_by_Id(authorname)
    for i in new_tweets:



        if i["id_str"] not in tweets_id_list:
            insert_one(authorname,i)
            print("new tweet inserted: ")
            print("tweeter: "+i["user"]["screen_name"])
            print("tweets id: "+ i["id_str"])
            print("created at: "+i["created_at"])

    return res

def check_newtweets_and_insert(authorlist):
    for i in authorlist:
        if mydb[i] == False:
            mydb[i]
        print("checking new tweets of "+i+"......")

        insert_new(i)
        print("...check finished...")

times = 0
while True:

    print("begin checking for the "+str(times)+ " time ......")
    print("start time: "+str(datetime.datetime.now()))
    check_newtweets_and_insert(get_authors())
    print("finish time: "+str(datetime.datetime.now()))
    time.sleep(300)
    times+=1