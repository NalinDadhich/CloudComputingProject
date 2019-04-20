from threading import Thread
from kafka import KafkaConsumer


class Consumer:
    def __init__(self, received_info):
        self.consumer = KafkaConsumer()
        self.thread = Thread(target=self.send_to_all)
        self.received_info = received_info

    def start(self):
        self.thread.start()

    def send_to_all(self):
        for m in self.consumer:
            self.received_info(m.value)
