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
    def __init__(self, c_id):
        consumer_key = ['W3nWSuPyudnw8142u58LNXiTc'][0]
        consumer_secret = ['cNTNL1tBB9lQKNaIr11u1CLv0IMBRzc81JS7QqRLCNXy6b334p'][0]
        access_token = ['3149835139-Ey1XqWLn6Mk1MFKcHbTtaDJ9NZUETZJYgISfLjW'][0]
        token_secret = ['Y0ZffGkSBbaYYSkvitsEunU9gyj2EAERWMxUhAaiPe30k'][0]

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, token_secret)

        self.api = tweepy.API(auth)
        self.analyzer = SentimentIntensityAnalyzer()

    def create_db(self, ip, name):
        url = ip + '/' + name
        r = requests.put(url)
        print(r.text)

    def clean_tweet(self,text):
        return ' '.join(re.sub("(@[A-Za-z0-9_-]+)|(\w+:\/\/\S+)"," ",text).split())

    def getSentimentScores(self, tweet):
        return self.analyzer.polarity_scores(tweet)['compound']

    def bulk_upload(self, ip, payload):
        headers = {'content-type': 'application/json'}
        url = ip + '/_bulk_docs'
        r = requests.post(url, data=payload, headers=headers)
        print(r.text)

    def limit_handled(self, cursor):
        while True:
            try:
                yield next(cursor)
            except tweepy.RateLimitError:
                time.sleep(15 * 60)
            except StopIteration:
                break
    
    
class RETHarvester(TwitterHarvester):
    def __init__(self, c_id):
        super().__init__(c_id)

    def harvest(self, n, query):
        tid = []
        created_at = []
        tweet_text = []
        retweet_counts = []
        favorite_count = []
        hashtags = []
        tweet_ss = []

        cursor = tweepy.Cursor(self.api.search,q=query,tweet_mode="extended").items(n)
        for t in cursor:
            tweet_info = t._json
            # only harvest non-retweeted tweets
            try:
                tweet_info['retweeted_status']
            except KeyError:
                text = self.clean_tweet(tweet_info['full_text'])
                ss = self.getSentimentScores(text)
                
                tid.append(tweet_info['id_str'])
                created_at.append(tweet_info['created_at'])
                tweet_text.append(text)
                retweet_counts.append(tweet_info['retweet_count'])
                favorite_count.append(tweet_info['favorite_count'])
                hashtags.append(tweet_info['entities']['hashtags'])
                tweet_ss.append(ss)    
        return tid, created_at, tweet_text, retweet_counts, favorite_count, hashtags, tweet_ss


    def prepare_data(self, tid, created_at, tweet_text, retweet_counts, favorite_count, hashtags, tweet_ss, city, topic):
        batch = []
        zipped = zip(tid, created_at, tweet_text, retweet_counts, favorite_count, hashtags, tweet_ss)
        for item in zipped:
            tweet = {}
            tweet['_id'] = item[0]
            tweet['city'] = city
            tweet['topic'] = topic
            tweet['created_at'] = item[1]
            tweet['text'] = item[2]
            tweet['retweet_count'] = item[3]
            tweet['favorite_count'] = item[4]
            tweet['hashtag'] = item[5]
            tweet['sentiment'] = item[6]
            batch.append(tweet)
        docs = {'docs': batch}
        docs = json.dumps(docs)
        return docs

class GEOHarvester(TwitterHarvester):
    def __init__(self, c_id):
        super().__init__(c_id)
    
    def harvest(self, city, max_id, n):
        tid = []
        created_at = []
        tweet_text = []
        retweet_counts = []
        favorite_count = []
        hashtags = []
        tweet_ss = []
        
        cursor = self.limit_handled(tweepy.Cursor(self.api.search,tweet_mode="extended", lang="en", geocode=city, max_id = max_id).items(n))
        for t in cursor:
            tweet_info = t._json
            try:
                tweet_info['retweeted_status']
            except KeyError:
                text = self.clean_tweet(tweet_info['full_text'])
                ss = self.getSentimentScores(text)

                tid.append(tweet_info['id_str'])
                created_at.append(tweet_info['created_at'])
                tweet_text.append(text)
                retweet_counts.append(tweet_info['retweet_count'])
                favorite_count.append(tweet_info['favorite_count'])
                hashtags.append(tweet_info['entities']['hashtags'])
                tweet_ss.append(ss)
            
        max_id = str(int(tid[-1])-1)
        return max_id, (tid, created_at, tweet_text, retweet_counts, favorite_count, hashtags, tweet_ss)

    def prepare_data(self, tid, created_at, tweet_text, retweet_counts, favorite_count, hashtags, tweet_ss, city):
        batch = []
        zipped = zip(tid, created_at, tweet_text, retweet_counts, favorite_count, hashtags, tweet_ss)
        for item in zipped:
            tweet = {}
            tweet['_id'] = item[0]
            tweet['city'] = city
            tweet['created_at'] = item[1]
            tweet['text'] = item[2]
            tweet['retweet_count'] = item[3]
            tweet['favorite_count'] = item[4]
            tweet['hashtag'] = item[5]
            tweet['sentiment'] = item[6]
            batch.append(tweet)
        docs = {'docs': batch}
        docs = json.dumps(docs)
        return docs


def collect_property_opinion(c_id, RET, db):
    city = ['melbourne', 'sydney', 'brisbane'][c_id]
    queries = ['buy house {}'.format(city) , 'house market {}'.format(city), 'house price {}'.format(city)]
    for query in queries:
        print(query)
        tid, created_at, tweet_text,retweet_counts, favorite_count, hashtags, tweet_ss = RET.harvest(50, query)
        docs = RET.prepare_data(tid, created_at, tweet_text,retweet_counts, favorite_count, hashtags, tweet_ss, city, query)
        # print(docs)
        RET.bulk_upload('http://admin:admin@172.26.134.87:5984/'+db, docs)


def collect_city_opinion(c_id, GEO, db):
    city_coor = ["-37.8136,144.9631,30km","-33.869,151.209,30km","-27.471,153.026,30km"][c_id]
    city = ['melbourne', 'sydney', 'brisbane'][c_id]
    max_id = None
    count = 0
    while count < 10:
        max_id, (tid, created_at, tweet_text, retweet_counts, favorite_count, hashtags, tweet_ss) = GEO.harvest(city_coor, max_id, 15)
        docs = GEO.prepare_data(tid, created_at, tweet_text, retweet_counts, favorite_count, hashtags, tweet_ss, city)
        GEO.bulk_upload('http://admin:admin@172.26.134.87:5984/'+db, docs)
        count += 1
        # print(docs)
        time.sleep(60)
    

def main():
    # get container id
    c_id = 2
    # c_id = int(os.environ.get('env_val')[-1])

    # GEO = GEOHarvester(c_id)
    RET = RETHarvester(c_id)

    # city_db = 'twitter-city'
    RET_db = 'twitter-property'
    # GEO.create_db('http://admin:admin@172.26.134.87:5984', city_db)
    # RET.create_db('http://admin:admin@172.26.134.87:5984', RET_db)

    collect_property_opinion(c_id, RET, RET_db)
    # collect_city_opinion(c_id, GEO, city_db)


if __name__ == "__main__":
    main()