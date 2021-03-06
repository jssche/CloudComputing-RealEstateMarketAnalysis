import couchdb
import time
import nltk
import re
from nltk.tokenize import TweetTokenizer
nltk.set_proxy('http://wwwproxy.unimelb.edu.au:8000/')
nltk.download('words')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import stopwords
import gensim


class TwCitytopicAnalyzer:
    def __init__(self, server_ip,username,password, city):
        serverAddress="http://%s:%s@%s:5984/" % (username, password, server_ip)
        self.server = couchdb.Server(serverAddress)
        self.dataDB = self.server["twitter-city"]

        # tokenizer & lemmatizer
        self.tt = TweetTokenizer()
        self.city = city
        self.stopwords = set(stopwords.words('english'))
        self.lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        self.words = set(nltk.corpus.words.words())  # a list of words provided by NLTK
        self.words = set([word.lower() for word in self.words])  # lowercase all the words for better matching

    def lemmatize(self, word):
        lemma = self.lemmatizer.lemmatize(word, 'v')
        if lemma == word:
            lemma = self.lemmatizer.lemmatize(word, 'n')
        return lemma

    def getAll(self, include_docs=True):
        data = []
        if include_docs:
            for item in self.dataDB.view('_all_docs',include_docs=True):
                data.append(item['doc'])
        else:
            for item in self.dataDB.view('_all_docs',include_docs=False):
                data.append(item.key)
        return data


    def topicanalysis(self,numTopics,numWords):
        data = self.getAll(include_docs=True)
        data_mel=[]
        data_syd=[]
        data_bne=[]
        # sort_bytime = sorted(data, key=lambda x: time.mktime(time.strptime(x['created_at'], '%a %b %d %H:%M:%S +0000  %Y')))
        for each in data:
            if self.city == "melbourne" and each['city'] == "melbourne":
                data_mel.append(each)
            elif self.city == "brisbane" and each['city'] == 'brisbane':
                data_bne.append(each)
            elif self.city == "sydney" and each ['city'] == 'sydney':
                data_syd.append(each)

        all ={}
        if len(data_mel) != 0:
            all["mel"] = self.preprocessedLDAmodel(data_mel,numTopics,numWords)
        if len(data_syd) != 0:
            all["syd"] = self.preprocessedLDAmodel(data_syd,numTopics,numWords)
        if len(data_bne) != 0:
            all["bne"] = self.preprocessedLDAmodel(data_bne, numTopics,numWords)


        return all



    def preprocessedLDAmodel(self,data,numTopics,numWords):

        data_text = []
        for i in data:
            each_text = i['text']
            twitter = re.sub(r"(@)\S+", "", each_text)
            twitter = re.sub(r"(https?\://|www)\S+", "", twitter)
            twitter = re.sub(r"\n", "", twitter)
            twitter = twitter.strip()
            preprocess = []
            for word in self.tt.tokenize(twitter):
                preprocess.append(word.lower())
            preprocess = list(filter(lambda ele: re.search("[a-zA-Z\s]+", ele) is not None, preprocess))
            preprocess = [w for w in preprocess if not w in self.stopwords]
            lemma_process = [self.lemmatize(w) for w in preprocess]
            data_text.append(lemma_process)
            dictionary = gensim.corpora.Dictionary(data_text)
            corpus = [dictionary.doc2bow(text) for text in data_text]
            lda = gensim.models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=numTopics)
            topics=[]
            for topic in lda.print_topics(num_words=numWords):
                topics.append(topic)
            return topics
