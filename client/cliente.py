import grpc

import message_broker_pb2
import message_broker_pb2_grpc

def run_client():
    channel = grpc.insecure_channel('localhost:50051')
    stub = message_broker_pb2_grpc.MessageBrokerServiceStub(channel)

    # Publicar un mensaje en un tema
    message_request = message_broker_pb2.MessageRequest(topic='tema1', message='Hola mundo!')
    message_response = stub.PublishMessage(message_request)
    print("Respuesta del servidor:", message_response.message)

    # Suscribirse a un tema y recibir mensajes
    topic_request = message_broker_pb2.TopicRequest(topic='tema1')
    message_stream = stub.SubscribeToTopic(topic_request)
    print("Mensajes recibidos:")
    for message in message_stream:
        print("Tema:", message.topic)
        print("Mensaje:", message.message)
        print()

if __name__ == '__main__':
    run_client()
