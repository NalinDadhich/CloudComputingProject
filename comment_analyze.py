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
        print("111111111111111111111")
        print(record)
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
            vote_count[video_id]["positive"] = 0
            vote_count[video_id]["neutral"] = 0
            vote_count[video_id]["negative"] = 0

        if sentiment['compound'] >= 0.05:
            print("\nPOSITIVVVVEEEEEEEEEEEEE")
            vote_count[video_id]["positive"] += 1

        elif sentiment['compound'] >= -0.05:
            print("\nNEUTRAALLLLLLLLLLLLL")
            vote_count[video_id]["neutral"] += 1
        else:
            print("\nNEGATIIVVEEEEEEEEEEEEEEEE")
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

    pkl_in = open("stats.pickle", "rb")
    vote_count = pkl.load(pkl_in)

    global time_stamps, all_v_id, v_id_positive, v_id_neutral, v_id_negative
    if len(time_stamps) == 0:
        time_stamps.append(0)
    else:
        time_stamps.append(time_stamps[-1] + 1)

    for v_id in vote_count.keys():
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

    # for v_id in vote_count.keys():
    #     plt.subplot(5,2,v_id)
    #     plt.bar()

    print("vote_count: ", vote_count)
    print("v_id_positive: ", v_id_positive)
    print("v_id_neutral: ", v_id_neutral)
    print("v_id_negative: ", v_id_negative)
    print("time stamps: ", time_stamps)
    print("\n")

    dump_csv(v_id_positive, v_id_neutral, v_id_negative)

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # for v_id_no, v_id in enumerate(vote_count.keys()):
        # plt.subplot(5,2,v_id_no+1)
        # plt.plot(time_stamps, v_id_positive[v_id])
        # plt.show()
        # break

        # plt.plot(time_stamps, v_id_positive[v_id])

    # plt.show()

    print("2222222222222222222222")
    for record in records:
        record[1] = record[1].encode('utf-8')
        producer.send('sa', '\t'.join([str(e) for e in record]).encode('utf-8'))


obj = CommentAnalysis()

# HERE CHANGE
# producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), bootstrap_servers='localhost:9092')

context = SparkContext(appName='SentimentAnalysis')
context.setLogLevel('WARN')
streaming_context = StreamingContext(context, 15)

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
streaming_context.awaitTerminationOrTimeout(10000)
streaming_context.stop(stopGraceFully=True)
