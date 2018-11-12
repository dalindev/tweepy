## What is this?

* data mining using tweepy (search by key words ex: 'trump')
* sentiment analysis using NLTK, textblob etc
* words frequence count from the batch of tweeter messages (remove stopwords and stemming)
* calling methods by API
  ```(ex: localhost:5000/search?query=trump&tweet_limit=100&word_freq=20)```

TODO: 
1. mysql for storeage
2. front-end page
3. get all tweets from one user's
4. proper auth


## Mining Twitter Data with python + mysql!

---

### To run you need:

1. python 3.7.0
2. MySQL
3. Twitter Account with consumer key and access token (get approved from twitter first)

Example of app_config.py file

### OAuth Authentication

```
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""
```

### Database

```
HOST = "127.0.0.1"
USER = "root"
PASSWD = "mypwd"
DATABASE = "twt_database"
```

### Installation

1. we need tweepy
2. we need TextBlob for sentiment analysis (note that NLTK download is about 3.5 GB)

```
pip install tweepy
pip install nltk
pip install textblob

$ python
>>> import nltk
>>> nltk.download()
```

We have to select “all” and click download.
