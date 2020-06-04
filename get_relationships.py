# COMP4641 Project code
# Written by TANG Wai Tin (Student ID: 20421717)
# Last Modified: 4 June 2020

import tweepy
import json
import sys
import csv
import pandas as pd
import time

TXT_FILE = "data/users.txt"

def getUserGroup(file):
  f = open(file)
  lines = f.read().split("\n")
  # print (lines)
  return lines

def getTweetAPI():
  # read file object
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

def isProtected(api, username):
  try:
    users = api.lookup_users(
        screen_names=[username],
    )
    return users[0]._json["protected"]
  except tweepy.TweepError:
    pass

def filterNonProtected(api, sc_names):
  new_names = []
  for i, v in enumerate(sc_names):
    if not isProtected(api, v):
      new_names.append(v)
    else:
      print ("{} is protected".format(v))
  return new_names

def getRelationships(sc_names, api):
  # get relationships network
  relaships = []
  for i, v in enumerate(sc_names):
    print ("Checking {}".format(v))
    j = i + 1
    while j < len(sc_names):
      A = v
      B = sc_names[j]
      try:
        # get friendship
        status = api.show_friendship(
            source_screen_name=A, 
            target_screen_name=B
        )
        if (status[0].following):
          relaships.append([A, B])
          print ("{} following {}".format(A, B))
        if (status[1].following):
          relaships.append([B, A])
          print ("{} following {}".format(B, A))
      except tweepy.TweepError:
        print ("Error in {} and {}".format(A, B))
        pass
      j = j + 1

  return relaships

api = getTweetAPI()
sc_names = getUserGroup(TXT_FILE)
relaships = getRelationships(sc_names, api)

net_folwers = pd.DataFrame(relaships)
net_folwers.columns = ["node", "following"]
net_folwers.to_csv("114_relationships.csv", index=False)