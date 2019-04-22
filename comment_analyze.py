from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer, NEGATE
from pyspark.streaming import StreamingContext
from pyspark import SparkContext
from pyspark.streaming.kafka import KafkaUtils

import nltk
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer, NEGATE
from nltk.stem import PorterStemmer
from nltk import WordNetLemmatizer
from kafka import KafkaProducer
from nltk.corpus import stopwords


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
        compound = self.find_sentiment(record[1])
        print(record)
        print(compound)
        return record + [compound]


def send_rdd(rdd):
    records = rdd.collect()
    for record in records:
        record[1] = record[1].encode('utf-8')
        producer.send('sa', '\t'.join([str(e) for e in record]))


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

# Send results through the producer
sentiments.foreachRDD(send_rdd)

streaming_context.start()
streaming_context.awaitTermination()
