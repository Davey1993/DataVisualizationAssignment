import json
from turtle import pd

import tweepy
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime as dt
import pandas as pd
from langdetect import detect
import matplotlib.pyplot as plt
# Authenticate to Twitter


analyzer = SentimentIntensityAnalyzer()

class MyStreamListener(tweepy.StreamListener):
   def __init__(self, api):
       self.api = api
       self.me = api.me()

   def on_status(self, tweet):
       print(f"{tweet.user.name}:{tweet.text}")

   def on_error(self, status):
       print("Error detected")



# Authenticate to Twitter
auth = tweepy.OAuthHandler("SP5coj65GrB18y8bCWzfwfCwP",
    "Eyfc8f1lO6egnNWcbKTdhUuiHu2dJUdpJOowUiSOP9fvMPKU2f")
auth.set_access_token("1306509707948044290-PpSTxhfHZPcTRItuQffd0JIiVmTpwy",
    "4aaoVNahES6CdT8KDMT9SVVhpocqH9alHC7mUAnzhhGTe")

# Create API object
api = tweepy.API(auth)
#aa = input("What do you want live information about\n")
#tweets_listener = MyStreamListener(api)
#stream = tweepy.Stream(api.auth, tweets_listener)
#stream.filter(track=[gaa], languages=["en"])
#with open('fetched_tweets.txt', 'a') as tf:
#    tf.write(stream)


topic = input("What topic do you want to apply sentiment analysis to?\n")
public_tweets = api.search(topic)

for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    score = analyzer.polarity_scores(topic)
    print("{:-<40} {}".format(topic, str(score)))
    with open('sentiment.json', 'a') as tf:
        # Write a new line
        tf.write('\n')

        # Write the json data directly to the file
        json.dump(score, tf)


#plt.plot(analysis.sentiment)
#plt.ylabel('Subjectivity')
#plt.xlabel('Polarity')
#plt.show()

