## Mining Twitter Data with python + mysql!

---

### To run you need:

1. python 2.7+
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
