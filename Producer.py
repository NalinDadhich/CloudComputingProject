import sys
sys.path.insert(0, "/Users/nalindadhich/Documents/4th_semester/CloudComputing/RealtimeSentimentAnalysis/youtube")
from kafka import KafkaProducer
from YT_Class import ExtractYouTube

class Producer:
    def __init__ (self, key, query, total_count):
        self.yt_class = ExtractYouTube(total_count, query, key,
                                       self.receive_comment)
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')

    def receive_comment(self, v_id, comment):
        self.producer.send('comments', bytes('{}\t{}'.format(v_id, comment),
                                             'utf-8'))
        print(v_id, comment)

