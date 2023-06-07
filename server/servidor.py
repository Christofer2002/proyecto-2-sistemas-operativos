import grpc
from concurrent import futures
import time
import queue
import logging

import message_broker_pb2
import message_broker_pb2_grpc

# Definición de la cola de mensajes por tema
message_queues = {}

# Implementación del servicio del message broker
class MessageBrokerServicer(message_broker_pb2_grpc.MessageBrokerService):
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def PublishMessage(self, request, context):
        topic = request.topic
        message = request.message

        # Verificar si el tema existe en la cola de mensajes
        if topic not in message_queues:
            message_queues[topic] = queue.Queue()
        
        # Insertar el mensaje en la cola del tema correspondiente
        message_queues[topic].put(message)

        response = message_broker_pb2.MessageResponse(success=True, message="Mensaje publicado con éxito")
        return response
    
    def SubscribeToTopic(self, request, context):
        topic = request.topic

        # Verificar si el tema existe en la cola de mensajes
        if topic not in message_queues:
            response = message_broker_pb2.Message()
            response.topic = topic
            response.message = "No hay mensajes disponibles en el tema"
            return response
        
        # Consumir mensajes de la cola del tema correspondiente
        while True:
            try:
                message = message_queues[topic].get(timeout=1)
                response = message_broker_pb2.Message()
                response.topic = topic
                response.message = message
                yield response
            except queue.Empty:
                break
    
# Configuración del servidor gRPC
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
