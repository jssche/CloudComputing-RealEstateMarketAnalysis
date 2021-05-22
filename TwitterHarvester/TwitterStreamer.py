import os
import re
import time
import json
import requests
import tweepy
from tweepy.streaming import StreamListener
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class  RETListener(StreamListener):

    def __init__(self, city, query, db):
        super().__init__()
        self.analyzer = SentimentIntensityAnalyzer()
        self.city = city
        self.query = query
        self.db_name = db

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
            # self.upload(tweet, t_id)

    def on_limit(self,status):
        print ("Rate Limit Exceeded, Sleep for 15 Mins")
        time.sleep(15 * 60)
        return True

    def on_error(self, status_code):
        print(status_code)
        return False

    def clean_tweet(self,text):
        return ' '.join(re.sub("(@[A-Za-z0-9_-]+)|(\w+:\/\/\S+)"," ",text).split())

    def getSentimentScores(self, tweet):
        return self.analyzer.polarity_scores(tweet)['compound']

    def upload(self, payload, doc_id):
        headers = {'content-type': 'application/json'}
        url = 'http://admin:admin@couchdbnode:5984/' + self.db_name + '/' + doc_id
        r = requests.put(url, data=payload, headers=headers)
        print(r.text)


class TwitterStreamer():
    def __init__(self, c_id, city, query, db):
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
        self.listener = RETListener(city, query, db)
        self.query = query

    def startStream(self):
        stream = tweepy.Stream(auth=self.api.auth, listener=self.listener, max_retries=3)
        try:
            print('Start streaming.')
            print(self.query)
            stream.filter(track=self.query)
        except KeyboardInterrupt as e :
            print("Stopped.")
        finally:
            print('Done.')
            stream.disconnect()


# def main():
#     # get container id
#     c_id = 0
#     # c_id = int(os.environ.get('env_val')[-1])
#     city = ['melbourne', 'sydney', 'brisbane'][c_id]

#     # generate query, query has to be in the format of of a list, eg. [q1, q2 ..]
#     query =  ['house price ' + city ]
#     RETStreamer = TwitterStreamer(c_id, city, query, 'twitter-property')
#     RETStreamer.startStream()

# if __name__ == "__main__":
#     main()


