from __future__ import absolute_import, print_function

# import pickle
# import pprint
# import json
# import string
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
from nltk.corpus import stopwords


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

    def tokenizing_tweet(self, tweet):
        """
        Tokenization:
        Using regular expression mentioned below we will remove HTML Tags,
        @Mentions, Hash Tags, URLs and various other irrelevant terms that
        provide no value in our analysis
        """
        return re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()

    def get_tweet_sentiment(self, tweet):
        """
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        """
        # punctuation = list(string.punctuation)
        swords = set(stopwords.words("english"))

        # print('1 --', tweet)

        # tokenizing tweet
        tweet = self.tokenizing_tweet(tweet)

        # print('2 --', tweet)

        # removing stopwords
        tweet = " ".join([term for term in tweet if term.lower() not in set(swords)])

        print('3 --', tweet)

        # create TextBlob object of passed tweet text
        analysis = textblob.TextBlob(tweet)

        return analysis.sentiment.polarity

    def get_tweets(self, query, count=100):
        """
        Main function to fetch tweets and parse them.
        """
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            """
            - lang (en)
            - result_type (mixed recent popular):
                * mixed : Include both popular and real time results in the response.
                * recent : return only the most recent results in the response
                * popular : return only the most popular results in the response.
            """
            fetched_tweets = self.api.search(
                q=query, lang="en", result_type="mixed", count=count
            )

            print(
                "[ Step 1 ] {0} <= Search [{1}] from twitter API".format(
                    len(fetched_tweets), query
                )
            )

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

            print("[ Step 2 ] {} <= unique tweets".format(len(tweets)))
            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query="black friday", count=10)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet["sentiment"] > 0]
    p_sum = sum([t["sentiment"] for t in ptweets])
    p_percentage = 100 * len(ptweets) / len(tweets)

    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet["sentiment"] < 0]
    n_sum = sum([t["sentiment"] for t in ntweets])
    n_percentage = 100 * len(ntweets) / len(tweets)

    # percentage of neutral tweets
    neu_percentage = 100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)

    print("[ Result ] Positive : {} %  Weight: {}".format(p_percentage, p_sum))
    print("[ Result ] Negative : {} %  Weight: {}".format(n_percentage, n_sum))
    print("[ Result ] Neutral  : {} % ".format(neu_percentage))
    print("[ Result ] Positive : {}".format(len(ptweets)))
    print("[ Result ] Negative : {}".format(len(ntweets)))
    print("[ Result ] Neutral  : {}".format(len(tweets) - len(ntweets) - len(ptweets)))
    print("[ Result ] Total => : {}".format(len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:5]:
        print(tweet["text"])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:5]:
        print(tweet["text"])


if __name__ == "__main__":
    # calling main function
    main()

