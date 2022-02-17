import json

import pandas as pd

import tweepy
import eel
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import keys

eel.init('web')


consumer_key = keys.API_key
consumer_secret = keys.API_key_secret
access_token = keys.Access_token
access_token_secret = keys.Access_token_secret


client = tweepy . Client (bearer_token = keys.bearer_token)

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

@eel.expose
def get_IDlist(filepath):
    df = pd.read_csv(filepath)
    IDList = df["ID"]
    IDList_str  = list(IDList)
    # for i in list(IDList):
    eel.init_page(IDList_str)

def make_df(response):
    return pd.DataFrame(response)

def pump_json(tweet):
    with open('tweet.json', 'a', encoding='utf-8') as f:
        json.dump(tweet, f)

@eel.expose
def tweet_getter(IDList):
    for id in IDList:
        # query = 'from:'+id+' -is:retweet'
        # tweets = client.search_recent_tweets(query=query, tweet_fields=['created_at',"author_id","id"],
        #                                      max_results=100)
        #
        #
        #
        # df = make_df(tweets.data)
        # df["author_name"] = id
        # # df.to_csv("../tweet_connecter/web/tweetCollection/"+id+".csv")
        #
        # dict = df.to_json(orient='records',force_ascii=False)
        # print(dict)
        #
        #
        # with open("../tweet_connecter/web/tweetCollection/"+id+".json", 'w') as write_f:
        #     json.dump(eval(dict), write_f, indent=4, ensure_ascii=False)
        public_tweets = api.user_timeline(screen_name=id)
        json_list = []
        for tweet in public_tweets:
            json_list.append(tweet)

        with open("../tweet_connecter/web/tweetCollection/"+id+".json", 'w') as write_f:
            jt = json.dump(json_list, write_f, indent=4, ensure_ascii=False)
            print(jt)

@eel.expose
def tweet_getter_by_Id(id):
    public_tweets = api.user_timeline(screen_name=id)
    json_list = []
    for tweet in public_tweets:
        json_list.append(tweet)

    eel.creat_tweet_list(json_list)

    return json_list

def get_tweetlist(filepath):
    tweetlist = os.listdir(filepath)
    return tweetlist

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





def run():
    IDList = get_IDlist("tweeter.csv")
    tweet_getter(IDList)
    tweetList = get_tweetlist("web/tweetCollection")
    keywords_distributor(tweetList)


# if __name__ == "__main__":
#     run()

eel.start('index.html',port=8888)


