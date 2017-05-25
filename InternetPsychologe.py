#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  InternetPsychologe.py
#  
#  Copyright 2017 Liam Hurwitz <liam@Deus>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import tweepy
from textblob import TextBlob
from sys import argv

print("Import finished...")

def get_api_access():
    """
    gets an authenticated twitter api accessor object
    Returns:
    api: authenticated twitter api accessor object
    """
    conf = yaml.load(open('APIKEYS/credentials.yml'))
    consumer_key= conf['user']['consumer_key']
    consumer_secret= conf['user']['consumer_secret']
    access_token=conf['user']['access_token']
    access_token_secret=conf['user']['access_token_secret']
   
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    return api

'''This function is implemented to handle tweepy exception errors
because search is rate limited at 180 queries per 15 minute window by twitter'''

def limit(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.TweepError as error:
            print(repr(error))
            print("Twitter Request limit error reached sleeping for 15 minutes")
            time.sleep(16*60)
        except tweepy.RateLimitError:
            print("Rate Limit Error occurred Sleeping for 16 minutes")
            time.sleep(16*60)

def retrieveTweets(api, search):
    '''Broken limit function
    if(lim == ""):
            lim = math.inf
    else:
        lim = int(lim)
    text = []'''
    for tweet in limit(tweepy.Cursor(api.search, q=search).items()):
        t = re.sub('\s+', ' ', tweet.text)
        text.append(t)

    data = {"Tweet":text,
            "Sentiment":"",
            "Score":""}

    dataFrame = pd.DataFrame(data, columns=["Tweet","Sentiment","Score"])

    return dataFrame

def analyze(al,dataFrame):
    sentiment = []
    score = []
    for i in range(0, dataFrame["Tweet"].__len__()):
        res = al.combined(text=dataFrame["Tweet"][i],
                          extract="doc-sentiment",
                          sentiment=1)
        sentiment.append(res["docSentiment"]["type"])
        if(res["docSentiment"]["type"] == "neutral"):
            score.append(0)
        else:
            score.append(res["docSentiment"]["score"])

    dataFrame["Sentiment"] = sentiment
    dataFrame["Score"] = score

    return dataFrame

def main():
    #Initialise Twitter Api
    api = get_api_access
    print("Hi , Im an Internet Psycho Script")
    print("I'd like to ask you a few questions.")
    #query = input("What can I give you information about on Twitter? ")
    
    #Retrieve tweets
    search = input("What can I give you information about on Twitter? (eg. #mothersday) : ")
    dataFrame = retrieveTweets(api,search)

    #Do Document Sentiment analysis
    dataFrame = analyze(al, dataFrame)

    #Save tweets, sentiment, and score data frame in csv file
    dataFrame.to_csv(input("Enter the name of the file (with .csv extension) : "))

if __name__ == '__main__':
    main()