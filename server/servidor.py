import grpc
from concurrent import futures
import time
import queue
import logging

import message_broker_pb2
import message_broker_pb2_grpc

# Definición de colas de mensajes por tema
message_queues = {
    'Noticias': queue.Queue(5),
    'Entretenimiento': queue.Queue(5),
    'Deportes': queue.Queue(5)
}


# Definición de clientes suscritos por tema
subscribed_clients = {
    'Noticias': set(),
    'Entretenimiento': set(),
    'Deportes': set()
}


# Implementación del servicio de intermediario de mensajes
class MessageBrokerServicer(message_broker_pb2_grpc.MessageBrokerServiceServicer):
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def PublishMessage(self, request, context):
        topic = request.topic
        message = request.message

        # Verificar si el tema existe en la cola de mensajes
        if topic not in message_queues:
            response = message_broker_pb2.MessageResponse(message="\nEl tema especificado no existe")
            return response

        # Insertar el mensaje en la cola correspondiente al tema
        if not message_queues[topic].full():
            message_queues[topic].put(message)
        else:
            response = message_broker_pb2.MessageResponse(message="\nEl tema especificado está lleno")
            return response

        response = message_broker_pb2.MessageResponse(message="\nMensaje publicado con éxito")
        return response

    
    def SubscribeToTopic(self, request, context):
        topic = request.topic

        # Verificar si el tema existe en la cola de mensajes
        if topic not in message_queues:
            response = message_broker_pb2.MessageResponse(message="\nEl tema especificado no existe")
            return response
        
        # Obtener el ID del cliente del contexto
        client_id = context.peer()

        # Agregar el cliente a los clientes suscritos al tema
        subscribed_clients[topic].add(client_id)

        response = message_broker_pb2.MessageResponse(message="\nSubscripción exitosa al tema: " + topic)
        return response
    

    def GetTopicList(self, request, context):
        topics = list(message_queues.keys())
        response = message_broker_pb2.TopicListResponse(topics=topics)
        return response
    

    def GetSubscribedTopicList(self, request, context):
        # Obtener el ID del cliente del contexto
        client_id = context.peer()

        # Encontrar los temas a los que el cliente está suscrito
        subscribed_topics = [topic for topic, clients in subscribed_clients.items() if client_id in clients]

        response = message_broker_pb2.TopicListResponse(topics=subscribed_topics)
        return response


# Configuración del servidor gRPC
def run_server():
    server = grpc.server(futures.ThreadPoolExecutor())
    message_broker_pb2_grpc.add_MessageBrokerServiceServicer_to_server(MessageBrokerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("\nServidor iniciado en el puerto 50051")
    print("Para detener el servidor, presione Ctrl + C")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_server()
