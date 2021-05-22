import json
import requests
import sys
import tweepy
from tweepy.streaming import StreamListener
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class  RETListener(StreamListener):

    def __init__(self):
        super().__init__()
        consumer_key = ['W3nWSuPyudnw8142u58LNXiTc'][0]
        consumer_secret = ['cNTNL1tBB9lQKNaIr11u1CLv0IMBRzc81JS7QqRLCNXy6b334p'][0]
        access_token = ['3149835139-Ey1XqWLn6Mk1MFKcHbTtaDJ9NZUETZJYgISfLjW'][0]
        token_secret = ['Y0ZffGkSBbaYYSkvitsEunU9gyj2EAERWMxUhAaiPe30k'][0]

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, token_secret)

        self.api = tweepy.API(auth)
        self.analyzer = SentimentIntensityAnalyzer()

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        print(status_code)
        return False


class TwitterStream():
    def __init__(self, c_id):
        consumer_key = ['W3nWSuPyudnw8142u58LNXiTc'][0]
        consumer_secret = ['cNTNL1tBB9lQKNaIr11u1CLv0IMBRzc81JS7QqRLCNXy6b334p'][0]
        access_token = ['3149835139-Ey1XqWLn6Mk1MFKcHbTtaDJ9NZUETZJYgISfLjW'][0]
        token_secret = ['Y0ZffGkSBbaYYSkvitsEunU9gyj2EAERWMxUhAaiPe30k'][0]

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, token_secret)

        self.api = tweepy.API(auth)
        self.analyzer = SentimentIntensityAnalyzer()
        self.listener = RETListener()

    def startStream(self):
        stream = tweepy.Stream(auth=self.api.auth, listener=self.listener)
        try:
            print('Start streaming.')
            stream.sample(languages=['en'])
        except KeyboardInterrupt as e :
            print("Stopped.")
        finally:
            print('Done.')
            stream.disconnect()

RETStream = TwitterStream(0)
RETStream.startStream()