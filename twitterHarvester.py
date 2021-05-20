import os
import re
import time
import json
import requests
import tweepy
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class TwitterHarvester():
    def __init__(self):
        _consumer_key = 'W3nWSuPyudnw8142u58LNXiTc'
        _consumer_secret = 'cNTNL1tBB9lQKNaIr11u1CLv0IMBRzc81JS7QqRLCNXy6b334p'
        _access_token = '3149835139-Ey1XqWLn6Mk1MFKcHbTtaDJ9NZUETZJYgISfLjW'
        _token_secret = 'Y0ZffGkSBbaYYSkvitsEunU9gyj2EAERWMxUhAaiPe30k'
        





def create_db(name):
    headers = {'content-type': 'application/json'}
    url = 'http://admin:admin@172.26.134.87:5984/' + name
    r = requests.put(url)
    print(r.text)



def main():
    # create_db('twitter')
    

    analyzer = SentimentIntensityAnalyzer()


if __name__ == "__main__":
    main()

