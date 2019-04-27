from threading import Thread
from kafka import KafkaConsumer


class Consumer:
    def __init__(self, received_info):

        # HERE CHANGE
        # self.consumer = KafkaConsumer('my_consumer')
        self._consumer = KafkaConsumer('my_consumer',
                                       bootstrap_servers=['localhost:9092'],
                                       auto_offset_reset='earliest',
                                       enable_auto_commit=True)
        self.thread = Thread(target=self.send_to_all)
        self.received_info = received_info

    def start(self):
        self.thread.start()

    def send_to_all(self):
        for m in self._consumer:
            self.received_info(m.value)
