# COMP4641 Project code
# Written by TANG Wai Tin (Student ID: 20421717)
# Last Modified: 4 June 2020

import pandas as pd
import tweepy
import os
import json

TWEET_COUNT = 3200
DATAPATH = "data/"
CSV_PATH = "want_to_die_10_redo_edited.csv"
ZERO_FILE = "non_suicidals"
ONE_FILE = "ideation_stages"
TWO_FILE = "absolute_want_suicides"

def preprocessCSV(filename):
    df = pd.read_csv(filename)
    columns = list(df.columns)

    edited_c_names = []
    for i in range(len(columns)):
        if i != 9:
            edited_c_names.append(columns[i])
        else:
            edited_c_names.append("Classification")

    df.columns = edited_c_names
    things_needed_df = df[["username", "Classification"]]
    return things_needed_df

def exportCSV(screen_name, Classification, data):
    columns = [
        "status_id",
        "reply_status_id",
        "reply_user_id",
        "is_quote_status",
        "lang",
        "created_at",
        "favorite_count",
        "retweet_count",
        "text"
    ]
    df = pd.DataFrame(data)
    df.columns = columns
    if Classification == 0:
        if not os.path.exists(ZERO_FILE):
            os.makedirs(ZERO_FILE)    
        path = ZERO_FILE + "/" + screen_name + ".csv"
        df.to_csv(path, index=False)
    elif Classification == 1:
        if not os.path.exists(ONE_FILE):
            os.makedirs(ONE_FILE)    
        path = ONE_FILE + "/" + screen_name + ".csv"
        df.to_csv(path, index=False)
    else:
        if not os.path.exists(TWO_FILE):
            os.makedirs(TWO_FILE)    
        path = TWO_FILE + "/" + screen_name + ".csv"
        df.to_csv(path, index=False)
        
def getTwitterAPI():
    f = open('secrets.json')
    secrets = json.load(f)
    # get the secrets
    consumer_key=secrets['consumer_key']
    consumer_secret=secrets['consumer_secret']
    access_token_key=secrets['access_token_key']
    access_token_secret=secrets['access_token_secret']
    # Connect API using secrets above
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(
        auth, 
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )

    return api

def recursive_timeline(api, username):
    tweets = []
    count = TWEET_COUNT
    for status in tweepy.Cursor(api.user_timeline, screen_name=username, count=count).items():
        tweets.append(status)
    return tweets

def print_specific_user_details(api, username):
    users = api.lookup_users(
        screen_names=[username],
    )
    for user in users:
        print (json.dumps(user._json, indent=4, sort_keys=True))

def is_user_protected(api, username):
    try:
        users = api.lookup_users(
            screen_names=[username],
        )
        return users[0]._json["protected"]
    except tweepy.TweepError:
        pass

def is_user_grabbed(username, Classification):
    if Classification == 0:
        return os.path.exists(ZERO_FILE + "/" + username + ".csv")
    elif Classification == 1:
        return os.path.exists(ONE_FILE + "/" + username + ".csv")
    else:
        return os.path.exists(TWO_FILE + "/" + username + ".csv")

def extract_timeline(api, username):
    tdata = []
    try:
        tweets = recursive_timeline(api, username)
        for t in tweets:
            td = t._json
            entity = [
                td["id_str"],
                td["in_reply_to_status_id_str"],
                td["in_reply_to_user_id_str"],
                td["is_quote_status"],
                td["lang"],
                td["created_at"],
                td["favorite_count"],
                td["retweet_count"],
                td["text"]
            ]
            tdata.append(entity)
    except tweepy.TweepError:
        pass
    return tdata
    

processed_df = preprocessCSV(DATAPATH + CSV_PATH)
api = getTwitterAPI()

for i, v in processed_df.iterrows():
    if is_user_grabbed(v["username"], v["Classification"]):
        continue
    else:
        if is_user_protected(api, v["username"]):
            continue
        print ("Grabbing {}".format(v["username"]))
        data = extract_timeline(api, v["username"])
        if len(data) != 0:
            exportCSV(v["username"], v["Classification"], data)
    