# COMP4641 Project code

Data collection - Official API Part

Author: TANG Wai Tin (Student ID: 20421717)

## About the code

The code here provides two crawling options by using official API OAuth key. Which includes:

1. Getting relationships: To get all in-network following / followers information
2. Getting user timeline: To get all recent 3200 tweets of each unprotected users

## Usage

The program requires ```tweepy``` package. Also, OAuth keys are required. The keys need to be seperately placed on a file ```secrets.json``` with the format like this:

```
{
    "consumer_key": <your_consumer_key>,
    "consumer_secret": <your_consumer_secret>,
    "access_token_key": <your_access_token>,
    "access_token_secret": <you_access_token_secret>
}
```

```get_relationships.py```: The program need to read a file on the ```data``` folder. Please place a ```txt``` format file containing the screen_names you want to scrape inside the file. Seperate each screen name with line break.

```get_timeline.py```: The program need to read a file on the ```data``` folder. Please place a ```csv``` format file containing two columns: ```Username``` and ```Classification```. First column indicates the screen name of the user and the second column indicates the suicidal group user belongs to.

## Remark

The program should run slow due to the Twitter official API rate limit.


Data collection and analysis - unofficial Twitter webscraper

Author: TAI Wai Ting (Student ID: 20340470)

##About the code

The code here utilizes unofficial Twitter webscraper (Twint, GetOldTweets3) to collect user information and construct a network.

```Twint.py```: The program reads a user in ```absolute_want_suicide``` folder, scraps the tweets from all accounts the user mentioned, and puts it into a folder named after the user. The program also filters through the scraped Tweets and put it inside "suicidal_tweets.csv".


```network_builder.py```: The program reads "suicidal_tweets.csv" and the users inside ```absolute_want_suicide``` to construct a network and perform numerous analyses.

## Remark

The directory should be modified for the code to work. 

Twint.py will encounter error after running for some time as the Twitter search engine blocks further query due to too high query rate. Wait for a few minutes and rerun, and it will continue on where it stopped. The data collection was performed using an automated script to rerun the code every 5 minutes after it stopped.
