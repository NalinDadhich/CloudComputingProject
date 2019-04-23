from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer, NEGATE
from pyspark.streaming import StreamingContext
from pyspark import SparkContext
from pyspark.streaming.kafka import KafkaUtils
import os
import nltk
import pickle as pkl
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer, NEGATE
from nltk.stem import PorterStemmer
from nltk import WordNetLemmatizer
from kafka import KafkaProducer
from nltk.corpus import stopwords
import matplotlib as plt

class CommentAnalysis:
    def __init__(self):
        self.stopwords = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.sia = SentimentIntensityAnalyzer()

    def find_sentiment(self, text):
        for neg in NEGATE:
            text = re.sub('(?i)' + re.escape(neg), neg, text)
        return self.sia.polarity_scores(text)

    def perform_sentiment_analysis(self, record):
        # print(record)
        sentiment = self.find_sentiment(record[1])
        print("andarrrrrrrrrrrrrrrrr")
        print(record)
        print(sentiment)
        video_id = record[0]

        exists = os.path.isfile('stats.pickle')
        if exists:
            pkl_in = open("stats.pickle", "rb")
            vote_count = pkl.load(pkl_in)
            pkl_in.close()
        else:
            vote_count = {}

        if video_id not in vote_count:
            vote_count[video_id] = {}
            vote_count[video_id]["positive"] = 0
            vote_count[video_id]["neutral"] = 0
            vote_count[video_id]["negative"] = 0

        if sentiment['compound'] >= 0.05:
            vote_count[video_id]["positive"] = vote_count[video_id][
                                                   "positive"] + 1

        elif sentiment['compound'] >= -0.05:
            vote_count[video_id]["neutral"] = vote_count[video_id][
                                                   "neutral"] + 1
        else:
            vote_count[video_id]["negative"] = vote_count[video_id][
                                                   "negative"] + 1
        print(vote_count)

        all_ids = [id for id in vote_count.keys()]
        # all_pos_perct = [float(100*vote_count[idt]["positive"]/(vote_count
        #             vote_count[idt]["positive"] + vote_count[idt]["negative"]))
        # for idt in vote_count.keys()]

        all_pos_percent = [100*float(vote_count[idt]["positive"]/(vote_count[
            idt]["positive"] + vote_count[idt]["negative"])) for idt in
                           vote_count.keys()]

        print(all_ids)
        print(all_pos_percent)

        for idx, ids in enumerate(all_ids):

        pkl_out = open("stats.pickle", "wb")
        pkl.dump(vote_count, pkl_out)
        pkl_out.close()


        return record + [sentiment]


def send_rdd(rdd):
    records = rdd.collect()
    print("111111111111111111111")

    for record in records:
        record[1] = record[1].encode('utf-8')
        producer.send('sa', '\t'.join([str(e) for e in record]).encode('utf-8'))


obj = CommentAnalysis()
producer = KafkaProducer(bootstrap_servers='localhost:9092')
context = SparkContext(appName='SentimentAnalysis')
context.setLogLevel('WARN')
streaming_context = StreamingContext(context, 5)

kvs = KafkaUtils.createDirectStream(streaming_context, ['comments'], {
    'bootstrap.servers': 'localhost:9092',
    'auto.offset.reset': 'smallest'
})


comments = kvs.map(lambda text: text[1].split('\t'))

sentiments = comments.map(lambda record: obj.perform_sentiment_analysis(record))
sentiments.pprint()
print("**********************************************************************")
# Send results through the producer
sentiments.foreachRDD(send_rdd)

streaming_context.start()
streaming_context.awaitTermination()
