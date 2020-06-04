#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:12:05 2020

@author: wtt
"""

import twint
import GetOldTweets3 as got
import csv

import os

directory = "/home/wtt/classification_timeline/absolute_want_suicides/"

class Tweet:
    
    def __init__(self, status_id, reply_status_id, reply_user_id, is_quote_status, lang\
                 , created_at, favorite_count, retweet_count, text):
        
        self.status_id = status_id
        self.reply_status_id = reply_status_id
        self.reply_user_id = reply_user_id
        self.is_quote_status = is_quote_status
        self.lang = lang
        self.created_at = created_at
        self.favorite_count = favorite_count
        self.retweet_count = retweet_count
        self.text = text

class OldTweet:    
    def __init__(self, date, username, to, replies, retweets, favorites,\
                                  text, mentions, formatted_date,\
                                  geo, hashtags, urls, permalink, ID, author_id):
        self.id = ID
        self.author_id = author_id
        self.date = date
        self.favorites = favorites
        self.formatted_date = formatted_date
        self.geo = geo
        self.hashtags = hashtags
        self.mentions = mentions
        self.permalink = permalink
        self.replies = replies
        self.retweets = retweets
        self.text = text
        self.to = to
        self.urls = urls
        self.username = username
        
class OldTweetPlus:    
    def __init__(self, date=None, username=None, to=None, replies=None, retweets=None, favorites=None,\
                                  text=None, mentions=None, formatted_date=None,\
                                  geo=None, hashtags=None, urls=None, permalink=None, ID=None, author_id=None, responder=None, suicidal=None):
        self.id = ID
        self.author_id = author_id
        self.date = date
        self.favorites = favorites
        self.formatted_date = formatted_date
        self.geo = geo
        self.hashtags = hashtags
        self.mentions = mentions
        self.permalink = permalink
        self.replies = replies
        self.retweets = retweets
        self.text = text
        self.to = to
        self.urls = urls
        self.username = username        
        self.responder = responder
        self.suicidal = suicidal
        
    def copy_from_old_tweet(self, old_tweet, responder):
        self.id = old_tweet.id
        self.author_id = old_tweet.author_id
        self.date = old_tweet.date
        self.favorites = old_tweet.favorites
        self.formatted_date = old_tweet.formatted_date
        self.geo = old_tweet.geo
        self.hashtags = old_tweet.hashtags
        self.mentions = old_tweet.mentions
        self.permalink = old_tweet.permalink
        self.replies = old_tweet.replies
        self.retweets = old_tweet.retweets
        self.text = old_tweet.text
        self.to = old_tweet.to
        self.urls = old_tweet.urls
        self.username = old_tweet.username        
        self.responder = responder
        
        
def saveOldTweets(filename,tweets):
    with open(filename, mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['date','username','to','replies','retweets','favorites','text',\
                              'mentions','formatted_date','geo','hashtags','urls','permalink', 'ID', 'author_id'])
        for tweet in tweets:
            file_writer.writerow([tweet.date, tweet.username, tweet.to,\
                                  tweet.replies, tweet.retweets, tweet.favorites,\
                                  tweet.text, tweet.mentions, tweet.formatted_date,\
                                  tweet.geo, tweet.hashtags, tweet.urls, tweet.permalink, tweet.id, tweet.author_id])

def saveOldTweetsPlus(filename,tweets):
    with open(filename, mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['date','username','to','replies','retweets','favorites','text',\
                              'mentions','formatted_date','geo','hashtags','urls','permalink', 'ID', 'author_id', 'RESPONDER'])
        for tweet in tweets:
            file_writer.writerow([tweet.date, tweet.username, tweet.to,\
                                  tweet.replies, tweet.retweets, tweet.favorites,\
                                  tweet.text, tweet.mentions, tweet.formatted_date,\
                                  tweet.geo, tweet.hashtags, tweet.urls, tweet.permalink, tweet.id, tweet.author_id, tweet.responder])
  
    
def loadTweets(filename):
    tweetOutput = []
    with open(filename) as file:
        file_reader = csv.reader(file, delimiter=',')
        linecount= 0
        for row in file_reader:
            linecount+=1
            if linecount == 1:
                continue #header line; ignore it
            else:
                    #print(str(i)+": "+row[i]+", " + str(type(row[i])))
                    #new_tweet = Tweet(row[3],row[4],row[2],row,[5],row[6],row[7],row[8],row[9],row[13],row[10],row[1],row[11],row[12],row[0])
                new_tweet = Tweet(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7], row[8])
                tweetOutput.append(new_tweet)
    return tweetOutput

def loadOldTweets(filename):
    tweetOutput = []
    with open(filename) as file:
        file_reader = csv.reader(file, delimiter=',')
        linecount= 0
        for row in file_reader:
            linecount+=1
            if linecount == 1:
                continue #header line; ignore it
            else:
                    #new_tweet = Tweet(row[3],row[4],row[2],row,[5],row[6],row[7],row[8],row[9],row[13],row[10],row[1],row[11],row[12],row[0])
                new_tweet = OldTweet(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14])
                tweetOutput.append(new_tweet)
    return tweetOutput

def loadOldTweetsPlus(filename):
    tweetOutput = []
    with open(filename) as file:
        file_reader = csv.reader(file, delimiter=',')
        linecount= 0
        for row in file_reader:
            linecount+=1
            if linecount == 1:
                continue #header line; ignore it
            else:
                    #new_tweet = Tweet(row[3],row[4],row[2],row,[5],row[6],row[7],row[8],row[9],row[13],row[10],row[1],row[11],row[12],row[0])
                new_tweet = OldTweet(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15])
                tweetOutput.append(new_tweet)
    return tweetOutput


def getResponders(tweetOutput):
    responders = []
    for tweet in tweetOutput:
        spliced_text = tweet.text.split()
        for word in spliced_text:
            if (word[0] == "@"):
                formatted_word = word[1:]
                if (word[-1] == ':'):
                    formatted_word = formatted_word[:-1]
                    if (formatted_word not in responders):
                        responders.append(formatted_word)
    return responders
        
def scrapTweets(username, path):
    #check if  file exists
    filename = path+username+".csv"
    if (not os.path.exists(filename)):
        tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                                                .setSince("2020-01-01")\
                                                .setUntil("2020-02-29")\
                                                .setMaxTweets(100)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        filtered_tweets = []
        for tweet in tweets:
            text = tweet.text.lower() #convert to lowercase
            #print(text)
            #filter text using specific keywords first
            suicidal_phrases = ["to take my own life", "want to die right now",\
                                        "have nothing to live for", "it's not worth it anymore",\
                                        "don't want to live anymore", "me want to kill myself",\
                                        "myself hate my life hate", "want to be here anymore",\
                                        "want it to be over", "want it all to end",\
                                        "wish could just fall asleep", "fall asleep and never wake",\
                                        "want to end it all", "just really want to die",\
                                        "rather die its not worth", "i'm sorry that im leaving",\
                                        "fuck trying to live normal","so why should continue living",\
                                        "don't want to live defeated", "to commit suicide within few",\
                                        "and pain anymore just can", "put an end to this",\
                                        "been self harming for years","bad really am worthless what",\
                                        "life is this miserable just"]
            for phrase in suicidal_phrases:
                if (phrase in text):
                    filtered_tweets.append(suicidal_phrases)
        saveOldTweets(filename, tweets)
        return filtered_tweets

def scrap_responders(responders, path):
    all_tweets = []
    if (not os.path.exists(path)):
        os.mkdir(path)
    for responder in responders:
        print(responder)
        filtered_tweets = scrapTweets(responder,path)
  
        if (filtered_tweets != None):
            all_tweets = all_tweets + filtered_tweets
    #add a token file, indicating that all responders are scrapped
    f = open(path+"finished_reading_all_responders", "w")
    f.close()
    return all_tweets

def collect_responders_suicidal_tweets(path):
    all_tweets = []
    print(path)
    filelist = os.listdir(path)
    for file in filelist:
        print(file)
        unfiltered_tweets = loadTweets(path+file)
        filtered_tweets = []
        suicidal_phrases = ["to take my own life", "want to die right now",\
                                        "have nothing to live for", "it's not worth it anymore",\
                                        "don't want to live anymore", "me want to kill myself",\
                                        "myself hate my life hate", "want to be here anymore",\
                                        "want it to be over", "want it all to end",\
                                        "wish could just fall asleep", "fall asleep and never wake",\
                                        "want to end it all", "just really want to die",\
                                        "rather die its not worth", "i'm sorry that im leaving",\
                                        "fuck trying to live normal","so why should continue living",\
                                        "don't want to live defeated", "to commit suicide within few",\
                                        "and pain anymore just can", "put an end to this",\
                                        "been self harming for years","bad really am worthless what",\
                                        "life is this miserable just"]
        for tweet in unfiltered_tweets:
            text = tweet.text.lower() 
            for phrase in suicidal_phrases:
                if (phrase in text):
                    filtered_tweets.append(suicidal_phrases)              
        
        if (filtered_tweets != []):
            all_tweets = all_tweets + filtered_tweets
    #saveOldTweets(path+"results.csv", all_tweets)
    return all_tweets

def filter_3_word(path):
    all_tweets = []
    filelist = os.listdir(path)
    count = 0
    for file in filelist:
        unfiltered_tweets = loadOldTweets(path+file)
        filtered_tweets = []
        suicidal_phrases = ["want to die", "to kill myself", "to commit suicide",
                            "want to kill", "can't live", "to end it", "i'm tired of",
                            "i hate myself", "end it all", "end my life", "take my own",
                            "kill myself and", "my death would", "to live anymore",
                            "about killing myself", "kill myself i", "never wake up",
                            "killing myself i", "stop the pain", "kill myself right",
                            "thoughts of suicide", "point in living", "worth it anymore",
                            "have nothing to", "wanted to die"]
        for tweet in unfiltered_tweets:
            text = tweet.text.lower() 
            count += 1
            for phrase in suicidal_phrases:
                if (phrase in text):
                    filtered_tweets.append(tweet)              
        
        if (filtered_tweets != []):
            all_tweets = all_tweets + filtered_tweets
    return all_tweets,count

def filter_all_tweets(directory):
    onlyfiles = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    all_tweets = []
    count = 0
    for file in onlyfiles:
        username = file[:-4]   
        #check if the user has already have its scrapping finished
        if (os.path.exists(directory + username)):
            if(os.path.exists(directory + username + "/finished_reading_all_responders")):
                path= directory+username+"/"
                filtered_tweets,num  = filter_3_word(path)
                count += num
                tweets_with_responder = []
                for tweet in filtered_tweets:
                    tweet_plus = OldTweetPlus()
                    tweet_plus.copy_from_old_tweet(tweet, username)
                    tweets_with_responder.append(tweet_plus)
                all_tweets = all_tweets + tweets_with_responder
    print(count)
    saveOldTweetsPlus("/home/wtt/classification_timeline/suicidal_tweets_so_far.csv", all_tweets)
    return all_tweets

def get_all_responders(directory):
    onlyfiles = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for file in onlyfiles:
        #only do the scrapping if we have not finished scrapping info from the reesponder
        username = file[:-4]
        if (not os.path.exists(directory + username + "/finished_reading_all_responders")):
            path = directory+username+"/"
            tweetOutput = loadTweets(directory+username +".csv")
            responders = getResponders(tweetOutput)
            all_tweets = scrap_responders(responders, path)
            collect_responders_suicidal_tweets(path)
            print("-----------------USER FINISHED--------------------")
    print("----------------------DONE--------------------------")
    return

directory = "/home/wtt/classification_timeline/absolute_want_suicides/"
get_all_responders(directory)
"""
filename = "aarushaaa.csv"
root = "aarushaaa/"
path = directory+root
tweetOutput = loadTweets(directory+filename)
responders = getResponders(tweetOutput)
all_tweets = scrap_responders(responders, path)
collect_responders_suicidal_tweets(path)
"""

filter_all_tweets(directory)