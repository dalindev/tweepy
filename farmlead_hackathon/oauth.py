from __future__ import absolute_import, print_function

import tweepy
import json
import emoji
import re
import decimal
import MySQLdb
from dateutil import parser
import sys

# Add the ptdraft folder path to the sys.path list
sys.path.append('/farmlead_hackathon')
from farmlead_hackathon import app_config


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
consumer_key=app_config.consumer_key
consumer_secret=app_config.consumer_secret
access_token=app_config.access_token
access_token_secret=app_config.access_token_secret

# == Database ==
HOST = app_config.HOST
USER = app_config.USER
PASSWD = app_config.PASSWD
DATABASE = app_config.DATABASE


#MONEY PARSER LIBRARY
__version__ = '0.0.1'

__all__ = ('price_str', 'price_dec',)

_CLEANED_PRICE_RE = re.compile('[+-]?(?:\d{1,3}[.,]?)+')
_FRACTIONAL_PRICE_RE = re.compile('^([\d.,]+)[.,](\d{1,2})$')

_not_defined = object()


def price_str(raw_price, default=_not_defined, dec_point='.'):
   """Search and clean price value.
   Convert raw price string presented in any localization
   as a valid number string with an optional decimal point.
   If raw price does not contain valid price value or contains
   more than one price value, then return default value.
   If default value not set, then raise ValueError.
   Examples:
       12.007          => 12007
       00012,33        => 12.33
       +1              => 1
       - 520.05        => -520.05
       1,000,777.5     => 1000777.5
       1.777.000,99    => 1777000.99
       1 234 567.89    => 1234567.89
       99.77.11.000,1  => 997711000.1
       NIO5,242        => 5242
       Not a MINUS-.45 => 45
         42  \t \n     => 42
                       => <default>
       1...2           => <default>
   :param str raw_price: string that contains price value.
   :param default: value that will be returned if raw price not valid.
   :param str dec_point: symbol that separate integer and fractional parts.
   :return: cleaned price string.
   :raise ValueError: error if raw price not valid and default value not set.
   """
   def _error_or_default(err_msg):
       if default == _not_defined:
           raise ValueError(err_msg)
       return default

   # check and clean
   if not isinstance(raw_price, str):
       return _error_or_default(
           'Wrong raw price type "{price_type}" '
           '(expected type "str")'.format(price_type=type(raw_price)))

   price = re.sub('\s', '', raw_price)
   cleaned_price = _CLEANED_PRICE_RE.findall(price)

   if len(cleaned_price) == 0:
       return _error_or_default(
           'Raw price value "{price}" does not contain '
           'valid price digits'.format(price=raw_price))

   if len(cleaned_price) > 1:
       return _error_or_default(
           'Raw price value "{price}" contains '
           'more than one price value'.format(price=raw_price))

   price = cleaned_price[0]

   # clean truncated decimal (e.g. 99. -> 99)
   price = price.rstrip('.,')

   # get sign
   sign = ''
   if price[0] in {'-', '+'}:
       sign, price = price[0], price[1:]
       sign = '-' if sign == '-' else ''

   # extract fractional digits
   fractional = _FRACTIONAL_PRICE_RE.match(price)
   if fractional:
       integer, fraction = fractional.groups()
   else:
       integer, fraction = price, ''

   # leave only digits in the integer part of the price
   integer = re.sub('\D', '', integer)

   # remove leading zeros (e.g. 007 -> 7, but 0.1 -> 0.1)
   integer = integer.lstrip('0')
   if integer == '':
       integer = '0'

   # construct price
   price = sign + integer
   if fraction:
       price = ''.join((price, dec_point, fraction))

   return price


def price_dec(raw_price, default=_not_defined):
   """Price decimal value from raw string.
   Extract price value from input raw string and
   present as Decimal number.
   If raw price does not contain valid price value or contains
   more than one price value, then return default value.
   If default value not set, then raise ValueError.
   :param str raw_price: string that contains price value.
   :param default: value that will be returned if raw price not valid.
   :return: Decimal price value.
   :raise ValueError: error if raw price not valid and default value not set.
   """
   try:
       price = price_str(raw_price)
       return decimal.Decimal(price)

   except ValueError as err:
       if default == _not_defined:
		raise err

   return default

# tweepy ----------------------

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# remove emoji
def give_emoji_free_text(text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])

    return clean_text

# store data
def store_twt_user(twt_id, screen_name, location, followers_count, friends_count, created_at):
    db=MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8")
    cursor = db.cursor()
    insert_query = "INSERT INTO twt_user (twt_id, screen_name, location, followers_count, friends_count, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (twt_id, screen_name, location, followers_count, friends_count, created_at))
    db.commit()
    cursor.close()
    db.close()
    return

def store_twt_tweet(twt_id, created_at, twt_text, entities_json, user_id):
    db=MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8")
    cursor = db.cursor()
    insert_query = "INSERT INTO twt_tweet (twt_id, created_at, text, entities_json, user_id) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (twt_id, created_at, twt_text, entities_json, user_id))
    db.commit()
    cursor.close()
    db.close()
    return


api = tweepy.API(auth)

user_timeline = api.user_timeline("agfinity", tweet_mode="extended")

for tweet in user_timeline:

    if hasattr(tweet, "retweeted_status"):
        text = give_emoji_free_text(tweet.retweeted_status.full_text)
    else:
        text = give_emoji_free_text(tweet.full_text)

    prices = re.findall('(?:[\$]{1}[,\d]+.?\d*)', text, re.MULTILINE)

    if len(prices) > 0:
    	for price in prices:
        	print("Found price: " + price)
    else:
        print("Skipped tweet")
        print(text)
        print("\n -------------- \n")
        continue

    print("Created At: " + str(tweet.created_at))
    print("ID: " + str(tweet.id))
    print("Text:\n" + text)

    entities = tweet.entities
    print("User Mentions: " + str(entities.get("user_mentions")))
    print("Hashtags: " + str(entities.get("hashtags")))
    print("URLs: " + str(entities.get("urls")))

    print("Retweet Count: " + str(tweet.retweet_count))
    if hasattr(tweet, "retweeted_status"):
        print("Retweeted From: " + str(tweet.retweeted_status.user.screen_name))

    print("\n -------------- \n")

# Get the User object for twitter...
# user = api.get_user('prairiegrainltd')

# print(user.id)
# print(user.screen_name)
# print(user.location)
# print(user.followers_count)
# print(user.friends_count)
# print(user.created_at)

# store_twt_user(
# 	user.id,
# 	user.screen_name,
# 	user.location,
# 	user.followers_count,
# 	user.friends_count,
# 	user.created_at
# )

# twitter_msg = api.user_timeline(screen_name='agvaluebrokers', count=150)

# for msg in twitter_msg:
# 	print('-------------------------------------------------------')

# 	#print(msg.id)
# 	#print(msg.created_at)
# 	print(msg.text)
# 	#print(msg.entities)
# 	#print(msg.user.id)
# 	try:
# 		print('prices'+price_str('msg.text'))
# 	except:
# 		continue

	# try:
	# 	store_twt_tweet(
	# 		msg.id,
	# 		msg.created_at,
	# 		msg.text,
	# 		json.dumps(msg.entities),
	# 		msg.user.id,
	# 	)
	# except:
	# 	continue



# output = json.dumps(user.__dict__)
# print(output)



# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
# api.update_status(status='Updating using OAuth authentication via Tweepy!')
