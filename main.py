from Producer import Producer

producer = Producer(10, 'Live videos',
                    'AIzaSyBCTFgcvoLfP96zU10CRQQsdRtxCCvJ0So')
producer.start()
print("Producer has started!")

# server = Server()
# server.start()
# print("Server started")


# def broadcast_msg(message):
#     for conn in server.all_connected():
#         conn.sendMessage(message)
#
#
# consumer = Consumer(broadcast_msg)
# consumer.start()
# print("Consumer started")
