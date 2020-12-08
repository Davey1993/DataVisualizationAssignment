import tweepy
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from twitter_credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_SECRET, ACCESS_TOKEN

##-----Authentication-----###
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
auth.secure = True
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
analyser = SentimentIntensityAnalyzer()



##-----Inputting Chosen Topic-----##

topic = input("What topic do you want to apply sentiment analysis to?\n")
searchQuery = topic

retweet_filter = '-filter:retweets'

q = searchQuery + retweet_filter
tweetsPerQry = 100
fName = 'tweets.txt'
sinceId = None

max_id = -1
maxTweets = 100

tweetCount = 0

##----This method writes the desired number of tweets to the tweets.txt file.----##

with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        tweets = []
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=q, lang="en", count=tweetsPerQry, tweet_mode='extended')

            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(str(tweet.full_text.replace('\n', '').encode("utf-8")) + "\n")

            tweetCount += len(new_tweets)
            max_id = new_tweets[-1].id

        except tweepy.TweepError as e:
            ## Just exit if any error
            print("some error : " + str(e))
            break



##----Removes Unwanted chars-----##
def clean(tweet):
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r'@[A-Za-z0–9]+', '', tweet)
    return tweet

##--reads tweets---##
def read_tweets(file_name):
    with open(file_name, 'r') as f:
        tweets = [clean(line.strip()) for line in f]
    f.close()
    return tweets

##-------Loading Tweets for Sentiment Analysis -----##

tweets = read_tweets(fName)
#print(tweets[2])
#print(TextBlob(tweets[2]).sentiment)

##------Experimenting with vader-------##
scores =[]
sentences = [tweets]

for sentence in sentences:
    score = analyser.polarity_scores(sentence)
    scores.append(score)

dataFrame= pd.DataFrame(scores)

#print(dataFrame)
dataFrame.mean()

##------Plotting Sentiment Graph--------##

polarity = lambda x: TextBlob(x).sentiment.polarity
subjectivity = lambda x: TextBlob(x).sentiment.subjectivity

tweet_polarity = np.zeros(len(tweets))
tweet_subjectivity = np.zeros(len(tweets))

for idx, tweet in enumerate(tweets):
    tweet_polarity[idx] = polarity(tweet)
    tweet_subjectivity[idx] = subjectivity(tweet)

sns.scatterplot(tweet_polarity,  # X-axis
                tweet_subjectivity,  # Y-axis
                s=50);

plt.title("Sentiment Analysis", fontsize=20)
plt.xlabel('Negative                  Positive ', fontsize=15)
plt.ylabel('Polarity                Subjectivity ', fontsize=15)
plt.tight_layout()
plt.show()

