import grpc
from concurrent import futures
import time
import queue
import logging

import message_broker_pb2
import message_broker_pb2_grpc

# Definition of message queues per topic
message_queues = {
    'Noticias': queue.Queue(),
    'Entretenimiento': queue.Queue(),
    'Deportes': queue.Queue()
}

# Implementation of the message broker service
class MessageBrokerServicer(message_broker_pb2_grpc.MessageBrokerServiceServicer):
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def PublishMessage(self, request, context):
        topic = request.topic
        message = request.message

        # Verify if the topic exists in the message queue
        if topic not in message_queues:
            response = message_broker_pb2.MessageResponse(message="\nEl tema especificado no existe")
            return response
        
        # Insert the message into the corresponding topic queue
        message_queues[topic].put(message)

        response = message_broker_pb2.MessageResponse(message="\nMensaje publicado con éxito")
        return response
    
    def SubscribeToTopic(self, request, context):
        topic = request.topic

        # Verify if the topic exists in the message queue
        if topic not in message_queues:
            response = message_broker_pb2.MessageResponse(message="\nEl tema especificado no existe")
            return response
        else:
            response = message_broker_pb2.MessageResponse(message="\nSubscripción exitosa al tema: " + topic)
            return response
    
    def CheckNewMessages(self, request, context):
        topic = request.topic

        # Verify if the topic exists in the message queue
        if topic in message_queues:
            has_new_messages = not message_queues[topic].empty()
        else:
            has_new_messages = False
        
        response = message_broker_pb2.CheckResponse(has_new_messages=has_new_messages)
        return response
    
    def GetTopicList(self, request, context):
        topics = list(message_queues.keys())
        response = message_broker_pb2.TopicListResponse(topics=topics)
        return response

# gRPC server configuration
def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_broker_pb2_grpc.add_MessageBrokerServiceServicer_to_server(MessageBrokerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado en el puerto 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_server()
