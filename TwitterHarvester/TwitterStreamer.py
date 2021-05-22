import json
import requests
import re
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
            text = self.clean_tweet(tweet_info['full_text'])
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

            tweet = json.dumps(tweet)
            self.upload(self.db_name, tweet, t_id)
            

    def on_error(self, status_code):
        print(status_code)
        return False

    def clean_tweet(self,text):
        return ' '.join(re.sub("(@[A-Za-z0-9_-]+)|(\w+:\/\/\S+)"," ",text).split())

    def getSentimentScores(self, tweet):
        return self.analyzer.polarity_scores(tweet)['compound']

    def upload(db_name, payload, doc_id):
        headers = {'content-type': 'application/json'}
        url = 'http://admin:admin@172.26.134.87:5984/' + db_name + '/' + doc_id
        r = requests.put(url, data=payload, headers=headers)
        print(r.text)


class TwitterStream():
    def __init__(self, c_id, city, query, db):
        consumer_key = ['W3nWSuPyudnw8142u58LNXiTc'][0]
        consumer_secret = ['cNTNL1tBB9lQKNaIr11u1CLv0IMBRzc81JS7QqRLCNXy6b334p'][0]
        access_token = ['3149835139-Ey1XqWLn6Mk1MFKcHbTtaDJ9NZUETZJYgISfLjW'][0]
        token_secret = ['Y0ZffGkSBbaYYSkvitsEunU9gyj2EAERWMxUhAaiPe30k'][0]

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, token_secret)

        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.analyzer = SentimentIntensityAnalyzer()
        self.listener = RETListener(city, query, db)
        self.query = query

    def startStream(self):
        stream = tweepy.Stream(auth=self.api.auth, listener=self.listener)
        try:
            print('Start streaming.')
            print(self.query)
            stream.filter(track=self.query)
        except KeyboardInterrupt as e :
            print("Stopped.")
        finally:
            print('Done.')
            stream.disconnect()


def main():
    # get container id
    c_id = 0
    # c_id = int(os.environ.get('env_val')[-1])
    city = ['melbourne', 'sydney', 'brisbane'][c_id]

    # generate query, query has to be in the format of of a list, eg. [q1, q2 ..]
    query =  ['house price ' + city ]
    RETStreamer = TwitterStream(c_id, city, query, 'twitter-property')
    RETStreamer.startStream()

if __name__ == "__main__":
    main()


