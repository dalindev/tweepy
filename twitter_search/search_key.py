# from __future__ import absolute_import, print_function

import tweepy
import json

# import emoji
# import re
# import decimal
# import MySQLdb
# from dateutil import parser
import sys

# Add the ptdraft folder path to the sys.path list
sys.path.append("/twitter_search")
from twitter_search import app_config

"""
--> To run this <--
1. you need a approved Twitter Account with key and token
2. you need local mysql database or nosql db
3. create the database, create the table or using script to do those

Example of app_config.py file

# == OAuth Authentication ==
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

# == Database ==
HOST = "127.0.0.1"
USER = "root"
PASSWD = "farmlead"
DATABASE = "farmlead_hack"
"""

# == OAuth Authentication ==
consumer_key = app_config.consumer_key
consumer_secret = app_config.consumer_secret
access_token = app_config.access_token
access_token_secret = app_config.access_token_secret

# == Database ==
HOST = app_config.HOST
USER = app_config.USER
PASSWD = app_config.PASSWD
DATABASE = app_config.DATABASE

# tweepy ----------------------

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# Creating the API object while passing in auth information
api = tweepy.API(auth)
# The search term you want to find
query = "FarmLead"
# Language code (follows ISO 639-1 standards)
language = "en"
# Calling the user_timeline function with our parameters
results = api.search(q=query, lang=language, count=15, show_user=True)
# foreach through all tweets pulled
for tweet in results:
    # printing the text stored inside the tweet object
    print(tweet.user.screen_name, "OBJ-----------:", tweet)

