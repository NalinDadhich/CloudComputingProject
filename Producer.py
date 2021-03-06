import sys
sys.path.insert(0, "/Users/nalindadhich/Documents/4th_semester/CloudComputing/RealtimeSentimentAnalysis/youtube")
from kafka import KafkaProducer
from YT_Class import ExtractYouTube


class Producer:
    def __init__ (self, total_count, query, key):
        self.yt_class = ExtractYouTube(total_count, query, key,
                                       self.receive_comment)
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                      batch_size=8192)

    def receive_comment(self, v_id, comment):
        self.producer.send('comments_1', bytes('{}\t{}'.format(v_id, comment),
                                             'utf-8'))

    def start(self):
        self.yt_class.get_all_vids()
        print('Video Ids:', self.yt_class.video_ids)
        self.yt_class.start()