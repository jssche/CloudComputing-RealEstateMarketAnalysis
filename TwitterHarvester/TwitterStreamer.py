import os
import re
import time
import json
import logging
import requests
import tweepy
from tweepy.streaming import StreamListener
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class  RETListener(StreamListener):

    def __init__(self, city, query, url):
        super().__init__()
        self.analyzer = SentimentIntensityAnalyzer()
        self.city = city
        self.query = query
        self.url = url

    def on_status(self, status):
        try:
            status.retweeted_status
        except AttributeError:
            tweet_info = status._json
            t_id = tweet_info['id_str']
            text = self.clean_tweet(tweet_info['text'])
            ss = self.getSentimentScores(text)

            tweet = {}
            tweet['city'] = self.city
            tweet['topic'] = self.query
            tweet['created_at'] = tweet_info['created_at']
            tweet['text'] = text
            tweet['retweet_count'] = tweet_info['retweet_count']
            tweet['favorite_count'] = tweet_info['favorite_count']
            tweet['hashtag'] = tweet_info['entities']['hashtags']
            tweet['sentiment'] = ss
            print(tweet)
            tweet = json.dumps(tweet)
            self.upload(tweet, t_id)

    def on_limit(self,status):
        logging.info ("Streamer rate limit exceeded, Sleep for 15 Mins")
        time.sleep(15 * 60)
        return True

    def on_error(self, status_code):
        logging.error("{} error occured during streaming, stopping the streamer now..".format(status_code))
        return False

    def clean_tweet(self,text):
        return ' '.join(re.sub("(@[A-Za-z0-9_-]+)|(\w+:\/\/\S+)"," ",text).split())

    def getSentimentScores(self, tweet):
        return self.analyzer.polarity_scores(tweet)['compound']

    def upload(self, payload, doc_id):
        headers = {'content-type': 'application/json'}
        url = self.url + '/' + doc_id
        r = requests.put(url, data=payload, headers=headers)
        logging.info("Uploading new tweet to database.. Status: {}".format(r.text))


class TwitterStreamer():
    def __init__(self, c_id, city, query, db, cdbUrl):
        url = cdbUrl + db
        consumer_key = ['W3nWSuPyudnw8142u58LNXiTc', 'wL5sumrKtFVWCeK6Sc9rhjUkt', 'ASqO5zC2V0BkRb6Lyih9lJouk'][c_id]
        consumer_secret = ['cNTNL1tBB9lQKNaIr11u1CLv0IMBRzc81JS7QqRLCNXy6b334p',
                           '931N28Rx14CBLJGQGrkSj9fBl4RQTJI7W6Gy8aN4bjMMmDxghE',
                           'cBFQDKFkXbcqpGJKYFrKZEVMhZsRafxm9XsVNptEk8mFJWOn9q'][c_id]
        access_token = ['3149835139-Ey1XqWLn6Mk1MFKcHbTtaDJ9NZUETZJYgISfLjW',
                        '1233990955939688451-e0tjVg2xMCpdjNT8agJ27KGcxhrPRV',
                        '768639445830553601-jDmJU2HW861HAWJSatfsCWL6hiVU15V'][c_id]
        token_secret = ['Y0ZffGkSBbaYYSkvitsEunU9gyj2EAERWMxUhAaiPe30k',
                        '3DykoaCQ8GtG0EgmOaywIPzSnw9Nk3alsC93hd7ohUT6U',
                        'NwqCafV1Hq4WTcy9Pp9QBT44vBFh85ckLMAJxQ78Qmqye'][c_id]

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, token_secret)

        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, proxy='http://wwwproxy.unimelb.edu.au:8000/')
        self.analyzer = SentimentIntensityAnalyzer()
        self.listener = RETListener(city, query, url)
        self.query = query

    def startStream(self):
        stream = tweepy.Stream(auth=self.api.auth, listener=self.listener, max_retries=100)
        try:
            try_count = 0 
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            logging.info('Start streaming at {}. Streaming query: {}'.format(current_time, self.query))
            stream.filter(track=self.query)
        except Exception as e :
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            logging.critical("Streamer could not connect to Twitter at {}, please restart...".format(current_time))
            logging.critical(str(e))
            if try_count < 3:
                logging.info("retry {}: restarting streaming...".format(try_count))
                stream = tweepy.Stream(auth=self.api.auth, listener=self.listener, max_retries=100)
                try_count += 1
        finally:
            logging.info('Done.')
            stream.disconnect()


