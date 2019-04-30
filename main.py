from Producer import Producer
from server_create import Server
from Consumer import Consumer

producer = Producer(10, 'Movie Trailers',
                    'AIzaSyAW4SYZW9AOchUBMeusAb3xEBw936sJcyc')
producer.start()
print("Producer has started!")

server = Server()
server.start()
print("Server started")


def broadcast_msg(message):
    for conn in server.all_connected():
        conn.sendMessage(message)


consumer = Consumer(broadcast_msg)
consumer.start()
print("Consumer started")
