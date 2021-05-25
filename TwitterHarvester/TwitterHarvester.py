import os
import re
import time
import json
import requests
import logging
import tweepy
import nltk
nltk.set_proxy('http://wwwproxy.unimelb.edu.au:8000/')
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from topicanalysis import TwCitytopicAnalyzer
from TwitterStreamer import TwitterStreamer


class TwitterHarvester():
    def __init__(self, c_id):
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

        self.api = tweepy.API(auth, proxy='http://wwwproxy.unimelb.edu.au:8000/', retry_count=100, retry_delay=60)
        self.analyzer = SentimentIntensityAnalyzer()

    def create_db(self, ip, name):
        url = ip + name
        r = requests.put(url)
        logging.info(r.text)

    def clean_tweet(self,text):
        return ' '.join(re.sub("(@[A-Za-z0-9_-]+)|(\w+:\/\/\S+)"," ",text).split())

    def getSentimentScores(self, tweet):
        return self.analyzer.polarity_scores(tweet)['compound']

    def bulk_upload(self, url, payload):
        headers = {'content-type': 'application/json'}
        url = url + '/_bulk_docs'
        r = requests.post(url, data=payload, headers=headers)
        logging.info(r.text)
        # print(r.text)
    
    def upload(self, ip, db, payload):
        headers = {'content-type': 'application/json'}
        url = ip + db 
        r = requests.post(url, data=payload, headers=headers)
        logging.info(r.text)
        # print(r.text)

    def limit_handled(self, cursor):
        while True:
            try:
                yield next(cursor)
            except tweepy.RateLimitError:
                logging.info ("Harvester rate limit exceeded, Sleep for 15 Mins")
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
        try:
            cursor = tweepy.Cursor(self.api.search,q=query,tweet_mode="extended").items(n) 
            for t in cursor:
                tweet_info = t._json
                # only harvest non-retweeted tweets
                try:
                    tweet_info['retweeted_status']
                except KeyError:
                    text = self.clean_tweet(tweet_info['full_text'])
                    ss = self.getSentimentScores(text)
                    if ss != 0:
                        tid.append(tweet_info['id_str'])
                        created_at.append(tweet_info['created_at'])
                        tweet_text.append(text)
                        retweet_counts.append(tweet_info['retweet_count'])
                        favorite_count.append(tweet_info['favorite_count'])
                        hashtags.append(tweet_info['entities']['hashtags'])
                        tweet_ss.append(ss)    
        except Exception as e:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            logging.critical("RETHarvester could not connect to Twitter at {}, please restart...".format(current_time))
            logging.critical(str(e))
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
        try:
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
        except Exception as e:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            logging.critical("GEOHarvester could not connect to Twitter at {}, please restart using max_id {}".format(current_time, max_id))
            logging.critical(str(e))

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


def collect_property_opinion(city, RET, cdbUrl, db, n):
    queries = ['house price {}'.format(city)]
    # 'buy house {}'.format(city) , 'house market {}'.format(city), 
    for query in queries:
        logging.info('Collecting property tweets using query: {}..'.format(query))
        tid, created_at, tweet_text,retweet_counts, favorite_count, hashtags, tweet_ss = RET.harvest(n, query)
        docs = RET.prepare_data(tid, created_at, tweet_text,retweet_counts, favorite_count, hashtags, tweet_ss, city, query)
        RET.bulk_upload(cdbUrl + db, docs)
        # print(docs)


def collect_city_opinion(city, city_coor, GEO, cdbUrl, db, batch, n):
    max_id = None
    count = 0
    while count < batch:
        if count % 5 == 0:
            logging.info('Collecting {} city tweets, batch {}'.format(city, count))
        max_id, (tid, created_at, tweet_text, retweet_counts, favorite_count, hashtags, tweet_ss) = GEO.harvest(city_coor, max_id, n)
        docs = GEO.prepare_data(tid, created_at, tweet_text, retweet_counts, favorite_count, hashtags, tweet_ss, city)
        GEO.bulk_upload(cdbUrl+ db, docs)
        count += 1
        # print(docs)
        time.sleep(61)


def start_streaming(c_id, city, cdbUrl):
    query =  ['house price ' + city ]
    RETStreamer = TwitterStreamer(c_id, city, query, '/twitter-property', cdbUrl)
    RETStreamer.startStream()
    

def main():
    logging.basicConfig(filename='harvesterLog',level=logging.INFO)
    CITIES = ['melbourne', 'sydney', 'brisbane']
    CITIES_COOR = ["-37.8136,144.9631,30km","-33.869,151.209,30km","-27.471,153.026,30km"]
    CITY_DB = '/twitter-city'
    RET_DB = '/twitter-property'
    TOPIC_DB = '/twitter-city-topic'
    # COUCHDB_IP= '172.26.134.87'
    COUCHDB_IP='couchdbnode'
    COUCHDB_URL = 'http://admin:admin@{}:5984'.format(COUCHDB_IP)

    # Get container id
    # c_id = 3
    c_id = int(os.environ.get('env_val')[-1])

    # If the master node (c_id = 1) finds any failed slave node, it will harvest data on behalf of the failed node.
    if c_id == 1:
        pass
    else:
        c_id -= 2 

        city = CITIES[c_id]
        city_coor = CITIES_COOR[c_id]

        # Collect twitter data 
        RET = RETHarvester(c_id)
        GEO = GEOHarvester(c_id)
        
        RET.create_db(COUCHDB_URL, RET_DB)
        GEO.create_db(COUCHDB_URL, CITY_DB)
        
        collect_property_opinion(city, RET, COUCHDB_URL, RET_DB, 50)
        collect_city_opinion(city, city_coor, GEO, COUCHDB_URL, CITY_DB, 300, 12)

        #Find the topics of each city and upload to db
        city_topics = json.dumps(TwCitytopicAnalyzer(COUCHDB_IP,'admin','admin',city).topicanalysis(1,20))
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        logging.info('Generated city topics at {}'.format(current_time))
        GEO.create_db(COUCHDB_URL, TOPIC_DB)
        GEO.upload(COUCHDB_URL, TOPIC_DB, city_topics)
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        logging.info('Uploaded city topics at {}'.format(current_time))

        start_streaming(c_id, city, COUCHDB_URL)



if __name__ == "__main__":
    main()