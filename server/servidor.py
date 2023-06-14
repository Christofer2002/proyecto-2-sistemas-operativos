import grpc
from concurrent import futures
import time
import queue
import logging
import threading
from datetime import datetime

import message_broker_pb2
import message_broker_pb2_grpc

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(message)s', filemode='a')

# Definition of message queues per topic
message_queues = {
    'Noticias': queue.Queue(5),
    'Entretenimiento': queue.Queue(5),
    'Deportes': queue.Queue(5)
}

# Definition of subscribed clients per topic
subscribed_clients = {
    'Noticias': set(),
    'Entretenimiento': set(),
    'Deportes': set()
}

# Lock for adding subscribed clients
client_lock = threading.Lock()
client_queues = {}

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

        # Insert the message into the corresponding client's topic queue
        if topic in subscribed_clients:
            for client_id in subscribed_clients[topic]:
                if not client_queues[client_id][topic].full():
                    client_queues[client_id][topic].put(message)
                    self.logger.info(f"Nuevo mensaje recibido en el tema {topic}: {message}")
                else:
                    response = message_broker_pb2.MessageResponse(message="\nLa cola del cliente está llena")
                    return response
        else:
            response = message_broker_pb2.MessageResponse(message="\nNo hay clientes suscritos al tema")
            return response

        response = message_broker_pb2.MessageResponse(message="\nMensaje publicado con éxito")
        return response

    
    def SubscribeToTopic(self, request, context):
        topic = request.topic

        # Verify if the topic exists in the message queue
        if topic not in message_queues:
            response = message_broker_pb2.MessageResponse(message="\nEl tema especificado no existe")
            return response
        
        # Get the client id from context
        client_id = context.peer()

        # Add the client to the subscribed clients for the topic
        with client_lock:
            subscribed_clients[topic].add(client_id)
            if client_id not in client_queues:
                client_queues[client_id] = {}
            client_queues[client_id][topic] = queue.Queue(5)
        self.logger.info(f"Nuevo cliente suscrito al tema: {topic}")

        response = message_broker_pb2.MessageResponse(message="\nSubscripción exitosa al tema: " + topic)
        return response
    
    def GetTopicList(self, request, context):
        topics = list(message_queues.keys())
        response = message_broker_pb2.TopicListResponse(topics=topics)
        return response
    
    def GetSubscribedTopicList(self, request, context):
        # Get the client id from context
        client_id = context.peer()

        # Find the topics subscribed by the client
        subscribed_topics = [topic for topic, clients in subscribed_clients.items() if client_id in clients]

        response = message_broker_pb2.TopicListResponse(topics=subscribed_topics)
        return response
    
    def ListenForNewMessages(self, request, context):
        topic = request.topic

        # Verify if the topic exists in the message queue
        if topic not in message_queues:
            response = message_broker_pb2.MessageResponse(message="\nEl tema especificado no existe")
            return response
        
        # Get the client id from context
        client_id = context.peer()

        # Check if the client is subscribed to the topic
        if client_id not in subscribed_clients[topic]:
            response = message_broker_pb2.MessageResponse(message="\nEl cliente no está suscrito al tema: " + topic)
            return response

        message_queue = client_queues[client_id][topic]

        # Listen for new messages in the topic queue
        while True:
            try:
                message = message_queue.get(timeout=5)  # Wait for 5 seconds for a new message
                self.logger.info(f"Mensaje enviado al subscriptor {client_id} en el tema {topic}: {message}")
                yield message_broker_pb2.MessageResponse(message=message)
            except queue.Empty:
                continue  # Continue listening for new messages

# gRPC server configuration
def run_server():
    server = grpc.server(futures.ThreadPoolExecutor())
    message_broker_pb2_grpc.add_MessageBrokerServiceServicer_to_server(MessageBrokerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Servidor iniciado en el puerto 50051...")
    print("Servidor iniciado en el puerto 50051...")
    print("Para detener el servidor, presione Ctrl + C")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        logging.info("Deteniendo el servidor...")
        server.stop(0)
        logging.info("Servidor detenido")

if __name__ == '__main__':
    run_server()
