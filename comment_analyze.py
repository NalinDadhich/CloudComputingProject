from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer, NEGATE
from pyspark.streaming import StreamingContext
from pyspark import SparkContext
from pyspark.streaming.kafka import KafkaUtils
import os
import csv
import nltk
import pickle as pkl
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer, NEGATE
from nltk.stem import PorterStemmer
from nltk import WordNetLemmatizer
from kafka import KafkaProducer
from nltk.corpus import stopwords
import time
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import json
from collections import OrderedDict

time_stamps = []
all_v_id = []
v_id_positive = OrderedDict()
v_id_neutral = OrderedDict()
v_id_negative = OrderedDict()

start_time = 0
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
        video_id = record[0]
        exists = os.path.isfile('stats.pickle')

        # if exists and os.path.getsize("stats.pickle") > 0:
        #     pkl_in = open("stats.pickle", "rb")
        #     vote_count = pkl.load(pkl_in)
        #     pkl_in.close()
        # else:
        #     vote_count = OrderedDict()

        if exists and os.path.getsize("stats.pickle") > 0:
                f =  open("stats.pickle", "rb")
                unpickler = pkl.Unpickler(f)
                # if file is not empty scores will be equal
                # to the value unpickled
                try:
                    vote_count = unpickler.load()
                except:
                    vote_count = OrderedDict()


        else:
            vote_count = OrderedDict()

        if video_id not in vote_count:
            vote_count[video_id] = {}
            vote_count["total_comments"] = 0
            vote_count[video_id]["positive"] = 0
            vote_count[video_id]["neutral"] = 0
            vote_count[video_id]["negative"] = 0

        vote_count["total_comments"] = vote_count["total_comments"]+1
        if sentiment['compound'] >= 0.05:
            vote_count[video_id]["positive"] += 1

        elif sentiment['compound'] >= -0.05:
            vote_count[video_id]["neutral"] += 1
        else:
            vote_count[video_id]["negative"] += 1

        pkl_out = open("stats.pickle", "wb")
        pkl.dump(vote_count, pkl_out)
        pkl_out.close()

        return record+[sentiment]


def dump_csv(v_id_positive, v_id_neutral, v_id_negative):
    with open('dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow("\n")
        writer.writerow(["Positive vote count: "])
        for key, value in v_id_positive.items():
            writer.writerow([key])
            writer.writerow(value)

        writer.writerow("\n")
        writer.writerow(["Neutral vote count: "])
        for key, value in v_id_neutral.items():
            writer.writerow([key])
            writer.writerow(value)

        writer.writerow("\n")
        writer.writerow(["Negative vote count: "])
        for key, value in v_id_negative.items():
            writer.writerow([key])
            writer.writerow(value)


def send_rdd(rdd):
    records = rdd.collect()
    end_time = time.time()

    pkl_in = open("stats.pickle", "rb")
    vote_count = pkl.load(pkl_in)

    end_time = time.time()
    print("total_time: ", end_time - start_time)
    print("total_comments: ", vote_count["total_comments"])
    print("total comments per sec: ", vote_count["total_comments"]/(
        end_time-start_time))
    global time_stamps, all_v_id, v_id_positive, v_id_neutral, v_id_negative
    if len(time_stamps) == 0:
        time_stamps.append(0)
    else:
        time_stamps.append(time_stamps[-1] + 1)

    for v_id in vote_count.keys():
        if v_id == "total_comments":
            continue

        all_v_id.append(v_id)
        if v_id not in v_id_positive:
            v_id_positive[v_id] = []
        v_id_positive[v_id].append(vote_count[v_id]["positive"])

        if v_id not in v_id_neutral:
            v_id_neutral[v_id] = []
        v_id_neutral[v_id].append(vote_count[v_id]["neutral"])

        if v_id not in v_id_negative:
            v_id_negative[v_id] = []
        v_id_negative[v_id].append(vote_count[v_id]["negative"])

    dump_csv(v_id_positive, v_id_neutral, v_id_negative)


obj = CommentAnalysis()

# HERE CHANGE
context = SparkContext(appName='SentimentAnalysis')
context.setLogLevel('WARN')
streaming_context = StreamingContext(context, 60)

kvs = KafkaUtils.createDirectStream(streaming_context, ['comments'], {
    'bootstrap.servers': 'localhost:9092',
    'auto.offset.reset': 'smallest'
})


comments = kvs.map(lambda text: text[1].split('\t'))

sentiments = comments.map(lambda record: obj.perform_sentiment_analysis(record))
sentiments.pprint()
print("**********************************************************************")
# Send results through the producer
start_time = time.time()
sentiments.foreachRDD(send_rdd)

streaming_context.start()
streaming_context.awaitTerminationOrTimeout(10000)
streaming_context.stop(stopGraceFully=True)
