#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 18:45:46 2020

@author: wtt
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:12:05 2020

@author: wtt
"""

import twint
import GetOldTweets3 as got
import csv
import networkx as nx
import os
import matplotlib.pyplot as plt
import collections
import math
from scipy.optimize import curve_fit

directory = "/home/wtt/classification_timeline_archive/absolute_want_suicides/"

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
                                  geo=None, hashtags=None, urls=None, permalink=None, ID=None, author_id=None, responder=None,suicidal=None):
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

class TwintTweet:    
    def __init__(self, ID, conversation_id, created_at, date, time, timezone,
                 user_id, username, name, classification, tweet, mentions, urls,
                 photos, replies_count, retweets_count, likes_count,
                 hashtags, cashtags, link, retweet, quote_url, video, near,
                 geo, source, user_rt_id, user_rt, retweet_id, reply_to):
        self.id = ID
        self.conversation_id = conversation_id
        self.created_at= created_at
        self.date=date
        self.time=time
        self.timezone=timezone
        self.user_id = user_id
        self.username = username
        self.name= name
        self.user_id = user_id
        self.username = username
        self.name = name
        self.classification = classification
        self.tweet = tweet
        self.mentions = mentions
        self.urls = urls
        #etc; only the username is useful 
        
        
def loadTwintTweets(filename):
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
                new_tweet = TwintTweet(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7], row[8], row[9],\
                                  row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17], row[18], row[19],\
                                  row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27], row[28], row[29])
                tweetOutput.append(new_tweet)
    return tweetOutput        
        
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
                new_tweet = OldTweetPlus(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16])
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

def getAllUsers(directory):
    #Get all users, with a list detailing the connection between users
    onlyfiles = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    G = nx.Graph()
    for file in onlyfiles:
        #only do the scrapping if we have finished scrapping info from the reesponder
        username = file[:-4]
        if (os.path.exists(directory + username + "/finished_reading_all_responders")):
            #get the name of all responders present
            G.add_node(username)
            path = directory+username+"/"
            tweetOutput = loadTweets(directory+username +".csv")
            responders = getResponders(tweetOutput)
            for responder in responders:
                G.add_node(responder)
                G.add_edge(username, responder)
    return G

def getAllSuicidalUsers(directory):
    onlyfiles = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    H = nx.DiGraph()
    all_users = []
    removed_users = ["elisiixn", "imlarixx", "novemberdad", "unxoreheartt", "lordlorelai", "pepper_tae"] #deactivated users
    for file in onlyfiles:
        #only do the scrapping if we have finished scrapping info from the reesponder
        username = file[:-4]
        if (os.path.exists(directory + username + "/finished_reading_all_responders")):
            #get the name of all responders present
            H.add_node(username) 
            H.nodes[username]["color"] = "green"
            #if username not in all_users:
            #    all_users.append(username)
    #add the dates from want_to_die_10_only_suicidal.csv
    green_tweet_output = loadTwintTweets("/home/wtt/classification_timeline_archive/want_to_die_10_only_suicidal.csv")
    for tweet in green_tweet_output:
        if tweet.username in H.nodes():
            if ("date" not in H.nodes[tweet.username]):
                H.nodes[tweet.username]["date"] = tweet.date[5:10]
            else:
                H.nodes[tweet.username]["date"] = min(H.nodes[tweet.username]["date"], tweet.date[5:10])
            
    #Check the suicidal_tweets_so_far.csv
    filtered_tweets = loadOldTweetsPlus("/home/wtt/classification_timeline_archive/suicidal_tweets.csv")
    for tweet in filtered_tweets:
        if (tweet.suicidal == '1' or tweet.suicidal =='2'):
            if (tweet.responder not in removed_users and tweet.username not in removed_users):
                H.add_node(tweet.username)
            #note: responder should already be added. If not, this is an error
                H.add_edge(tweet.responder, tweet.username)
                if ("date" not in H.nodes[tweet.username]):
                    H.nodes[tweet.username]["date"] = tweet.date[5:10]
                else:
                    H.nodes[tweet.username]["date"] = min(H.nodes[tweet.username]["date"], tweet.date[5:10])
                H.nodes[tweet.responder]["color"] = "green"
                H.nodes[tweet.username]["color"] = "blue"
            #if tweet.username not in all_users:
            #    all_users.append(tweet.username)
    #Also try to add who the secondary users responded to
    
    for tweet in filtered_tweets:
        if (tweet.suicidal == '1' or tweet.suicidal =='2'):
            username = tweet.username
            source = tweet.responder
            if (os.path.exists(directory + source + "/" + username + ".csv")):
                tweetOutput = loadTweets(directory + source + "/" + username + ".csv")
                responders = getResponders(tweetOutput)
                for responder in responders:
                    if responder in H.nodes():
                        H.add_edge(username, responder)
    #remove the six deactivated users

    #Add the edges
    with open("114_relationships.csv") as file:
        file_reader = csv.reader(file, delimiter=',')
        linecount= 0
        for row in file_reader:
            linecount+=1
            if linecount == 1:
                continue #header line; ignore it
            else:
                #If the color of the node is undefined for now, the node came from a green node following a green node
                H.add_edge(row[0], row[1])
                #if ("color" not in H.nodes[row[0]]):
                #    H.nodes[row[0]]["color"] = "green"
                #if ("color" not in H.nodes[row[1]]):
                #    H.nodes[row[1]]["color"] = "green"                    
    #remove nodes with zero degree  
    for node, degree in list(H.degree()):
        if degree == 0:
            H.remove_node(node)
    H.remove_nodes_from(removed_users)
    return H#,all_users   
        
def save_users(all_users):
    with open('users.txt', 'w') as file:
        for user in all_users:
            file.writelines(user+"\n")

def func(x, a, c):
    return c*x**a   
         
def plot_degree_distribution(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    # print "Degree sequence", degree_sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    #logcnt = [math.log(cnt[i]) for i in range(len(cnt))]
    print(deg, cnt)
    
    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')
    #plt.loglog(deg, cnt)
    
    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)
    
    x = [deg[len(deg)-1-i] for i in range(len(deg))]
    y = [cnt[len(deg)-1-i] for i in range(len(deg))]
    #popt, pcov = curve_fit(func, x, y) #yields popt = [1.00721884, 32.36683178]]
    popt = np.array([-1.00721884, 32.36683178]) #parameter came from scipy.curve_fit
    
    plt.plot(x,func(x,*popt), label="fit: 32.366 * x ^ -1.007")
    # draw graph in inset
    #plt.axes([0.4, 0.4, 0.5, 0.5])
    #Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
    #pos = nx.spring_layout(G)
    #plt.axis('off')
    #nx.draw_networkx_nodes(G, pos, node_size=20)
    #nx.draw_networkx_edges(G, pos, alpha=0.4)
    
    plt.legend()
    plt.show()
    return deg, cnt

def centrality_test(G):
    deg_cent = {name: cent for name, cent in sorted(nx.degree_centrality(H).items(), key = lambda x:x[1], reverse=True)}
    betweenness_cent = {name: cent for name, cent in sorted(nx.betweenness_centrality(H).items(), key = lambda x:x[1], reverse=True)}
    closeness_cent = {name: cent for name, cent in sorted(nx.closeness_centrality(H).items(), key = lambda x:x[1], reverse=True)}
    return deg_cent, betweenness_cent, closeness_cent
"""
def draw_weakly_connected_components(G):
    largest_components=G.subgraph(sorted(nx.weakly_connected_components(G), key=len, reverse=True)[0])
    for index,component in enumerate(largest_components):
        nx.draw(component)
        #nx.savefig('fig{}.pdf'.format(index))
        plt.clf()
"""
            
H = getAllSuicidalUsers(directory)
#save_users(all_users)
#deg, cnt = plot_degree_distribution(H)
node_color = []
for node in H.nodes(data=True):
    if node[1]["color"] == "green":
        node_color.append("green")
    else:
        node_color.append("blue")

#pos = nx.spring_layout(H,k=0.15,iterations=20)    
#nx.draw(H,pos, node_color = node_color, node_size=100)
labels = nx.get_node_attributes(H, "date") 

pos = nx.kamada_kawai_layout(H)
pos_higher = {} #draw the labels slightly off the nodes for better readability
x_off = -0.06
y_off = 0.08  # offset on the y axis
for k, v in pos.items():
    pos_higher[k] = (v[0]+x_off, v[1]+y_off)
#nx.draw(H, pos=pos, node_color=node_color, node_size=100)
#nx.draw_networkx_labels(H, pos = pos_higher, labels=labels)
deg_cent, betweenness_cent, closeness_cent = centrality_test(H)
#draw_weakly_connected_components(H)


#Plot only largest weakly connected component
node_color = []
for node in H_sub.nodes(data=True):
    if node[1]["color"] == "green":
        node_color.append("green")
    else:
        node_color.append("blue")

H_sub = H.subgraph(max(nx.weakly_connected_components(H),key=len))
pos = nx.spring_layout(H_sub,k=0.3,iterations=20)    #nx.kamada_kawai_layout(H_sub)
pos_higher = {} #draw the labels slightly off the nodes for better readability
labels = nx.get_node_attributes(H_sub, "date") 
x_off = -0.06
y_off = 0.08  # offset on the y axis
for k, v in pos.items():
    pos_higher[k] = (v[0]+x_off, v[1]+y_off)
nx.draw(H_sub, pos=pos, node_color=node_color, edge_color = "lightgrey", node_size=100)
nx.draw_networkx_labels(H_sub, pos = pos_higher, labels=labels)
plt.savefig("graphwithdate.png")