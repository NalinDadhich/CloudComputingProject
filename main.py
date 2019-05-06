from Producer import Producer

producer = Producer(10, 'Movie trailers',
                    'AIzaSyC2xIrmR8u33LTINpCvpuLttNZJPuFEI0o')
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
