from __future__ import absolute_import, print_function

import pickle
import pprint
import json
import string
import re

import tweepy
import nltk
import textblob

# import emoji
# import re
# import decimal
# import MySQLdb

# from dateutil import parser
import sys

# Add the ptdraft folder path to the sys.path list
sys.path.append("/twitter_search")
from twitter_search import app_config


class TwitterClient(object):
    """
    Generic Twitter Class for sentiment analysis. s
    """

    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = app_config.consumer_key
        consumer_secret = app_config.consumer_secret
        access_token = app_config.access_token
        access_token_secret = app_config.access_token_secret

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

        # == Database ==
        HOST = app_config.HOST
        USER = app_config.USER
        PASSWD = app_config.PASSWD
        DATABASE = app_config.DATABASE

        # Creating the API object while passing in auth information
        # api = tweepy.API(self.auth)
        # # The search term you want to find
        # query = "FarmLead"
        # # Language code (follows ISO 639-1 standards)
        # language = "en"
        # # Calling the user_timeline function with our parameters
        # results = api.search(q=query, lang=language, count=15, show_user=True)
        # # foreach through all tweets pulled
        # for tweet in results:
        #     # getting tweet text
        #     try:
        #         tweetText = tweet["extended_tweet"]["full_text"]
        #     except AttributeError:
        #         tweetText = tweet["text"]

        #     # printing the text stored inside the tweet object
        #     print(tweet.user.screen_name, "OBJ-----------:", tweetText)

    def clean_tweet(self, tweet):
        """ 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        """
        return " ".join(
            re.sub(
                "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet
            ).split()
        )

    def get_tweet_sentiment(self, tweet):
        """ 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        """
        # create TextBlob object of passed tweet text
        analysis = textblob.TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"

    def get_tweets(self, query, count=100):
        """ 
        Main function to fetch tweets and parse them. 
        """
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                try:
                    parsed_tweet["text"] = tweet.extended_tweet.full_text
                except AttributeError:
                    parsed_tweet["text"] = tweet.text

                # saving sentiment of tweet
                parsed_tweet["sentiment"] = self.get_tweet_sentiment(
                    parsed_tweet["text"]
                )

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query="Donald Trump", count=100)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet["sentiment"] == "positive"]
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet["sentiment"] == "negative"]
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print(
        "Neutral tweets percentage: {} % ".format(
            100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)
        )
    )

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:100]:
        print(tweet["text"])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:100]:
        print(tweet["text"])


if __name__ == "__main__":
    # calling main function
    main()

