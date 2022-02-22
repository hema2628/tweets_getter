import datetime
import json

import pymongo

import eel
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from databaseMethods import DBMethods_authorinfo

eel.init('web')


# consumer_key = keys.API_key
# consumer_secret = keys.API_key_secret
# access_token = keys.Access_token
# access_token_secret = keys.Access_token_secret
#
#
# client = tweepy . Client (bearer_token = keys.bearer_token)
#
# auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
#
#
# api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

tweets_db = myclient["tweets"]
tweeters_db = myclient["tweeters_info"]
tweetersinfo = tweeters_db["tweeters_info"]

@eel.expose
def get_IDlist():

    authorsList = DBMethods_authorinfo.get_authors_from_database()

    eel.init_page(authorsList)
    return authorsList


@eel.expose
def tweet_getter_by_Id(id):

    time_period = get_time()

    myquery_author = {"screen_name":id}
    author = tweetersinfo.find_one(myquery_author)
    start_date = time_period["start_time"]
    end_time = time_period["end_time"]


    public_tweets = tweets_db[id].find().sort("_id",-1).limit(20)
    json_list = []
    for tweet in public_tweets:
        # tweet['text'] = text_translator(tweet['text'])
        json_list.append(tweet)


    res_dict = {"author":author,
                "tweets":json_list}

    eel.creat_tweet_list(res_dict)

    return json_list



def keywords_distributor(tweetfile):
    for file in tweetfile:
        # print(file)
        # df = pd.read_csv("../tweet_connecter/web/tweetCollection/"+file)
        # textslist = df["text"]
        # dates = df["created_at"]
        # filename = file.split(".")[0]
        # nlp.get_wordtype(df, textslist, dates, filename)

        with open("../tweet_connecter/web/tweetCollection/"+file,'r') as load_f:
            load_dict = json.load(load_f)

def get_time():
    end_time = datetime.datetime.now()
    start_time = end_time + datetime.timedelta(days= -1)
    time_period = {
        "start_time":start_time,
        "end_time":end_time
    }

    return time_period


eel.start('index.html',port=8888)
