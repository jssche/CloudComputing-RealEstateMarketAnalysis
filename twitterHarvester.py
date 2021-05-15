import os
import json
import requests
import tweepy

consumer_key = 'W3nWSuPyudnw8142u58LNXiTc'
consumer_secret = 'cNTNL1tBB9lQKNaIr11u1CLv0IMBRzc81JS7QqRLCNXy6b334p'
access_token = '3149835139-Ey1XqWLn6Mk1MFKcHbTtaDJ9NZUETZJYgISfLjW'
token_secret = 'Y0ZffGkSBbaYYSkvitsEunU9gyj2EAERWMxUhAaiPe30k'

callback_url = 'oob' # our url

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, token_secret)
api = tweepy.API(auth)

cursor = tweepy.Cursor(api.user_timeline,id='RayWhiteGroup').items(30)
for i in cursor:
    print(i.created_at)

