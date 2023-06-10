import grpc

import message_broker_pb2
import message_broker_pb2_grpc

import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

subscription_list = []

def PublishMessage(stub):
    topic_list = GetTopicList(stub)

    while True:
        print("\nTemas disponibles:")
        for i in range(len(topic_list)):
            print(" " + str(i + 1) + ". " + topic_list[i])
        topic_index = input("\nIngrese el tema: ")
        if topic_index.isdigit() and int(topic_index) > 0 and int(topic_index) <= len(topic_list):
            topic = topic_list[int(topic_index) - 1]
            break
        else:
            print("\nTema inválido. Por favor, intente nuevamente.")

    message = input("Ingrese el mensaje: ")
    message_request = message_broker_pb2.MessageRequest(topic=topic, message=message)
    message_response = stub.PublishMessage(message_request)
    print(message_response.message)

def SubscribeToTopic(stub):
    topic_list = GetTopicList(stub)

    while True:
        print("\nTemas disponibles:")
        for i in range(len(topic_list)):
            print(" " + str(i + 1) + ". " + topic_list[i])
        topic_index = input("\nIngrese número el tema al que desea suscribirse: ")
        if topic_index.isdigit() and int(topic_index) > 0 and int(topic_index) <= len(topic_list):
            topic = topic_list[int(topic_index) - 1]
            break
        else:
            print("\nTema inválido. Por favor, intente nuevamente.")
            
    topic_request = message_broker_pb2.TopicRequest(topic=topic)
    message_response = stub.SubscribeToTopic(topic_request)
    subscription_list.append(topic)
    print(message_response.message)

def CheckNewMessages(stub):

    while True:
        if len(subscription_list) == 0:
            print("\nNo se ha suscrito a ningún tema. Por favor, suscríbase a un tema primero.")
            return
        print("\nSuscripciones:")
        for i in range(len(subscription_list)):
            print(" " + str(i + 1) + ". " + subscription_list[i])
        topic_index = input("\nIngrese el tema para verificar si hay nuevos mensajes: ")
        if topic_index.isdigit() and int(topic_index) > 0 and int(topic_index) <= len(subscription_list):
            topic = subscription_list[int(topic_index) - 1]
            break
        else:
            print("\nTema inválido. Por favor, intente nuevamente.")

    check_request = message_broker_pb2.CheckRequest(topic=topic)
    check_response = stub.CheckNewMessages(check_request)
    if check_response.has_new_messages:
        print("Nuevos mensajes disponibles para el tema:", topic)
    else:
        print("\nNo hay nuevos mensajes para el tema:", topic)

def GetTopicList(stub):
    topic_list_request = message_broker_pb2.TopicListRequest()
    topic_list_response = stub.GetTopicList(topic_list_request)
    topic_list = list(topic_list_response.topics)
    return topic_list


def run_client():
    channel = grpc.insecure_channel('localhost:50051')
    stub = message_broker_pb2_grpc.MessageBrokerServiceStub(channel)

    while True:
        print("\nMenú:")
        print(" 1. Publicar un mensaje en un tema")
        print(" 2. Suscribirse a un tema")
        print(" 3. Verificar nuevos mensajes en un tema suscrito")
        print(" 4. Obtener lista de temas")
        print(" 5. Salir")
        choice = input("\nIngrese su elección: ")

        if choice == "1":
            PublishMessage(stub)
        elif choice == "2":
            SubscribeToTopic(stub)
        elif choice == "3":
            CheckNewMessages(stub)
        elif choice == "4":
            topic_list = GetTopicList(stub)
            print("\nLista de temas:")
            for i in range(len(topic_list)):
                print(" " + str(i + 1) + ". " + topic_list[i])
        elif choice == "5":
            break
        else:
            print("\nOpción inválida. Por favor, intente nuevamente.")

if __name__ == '__main__':
    run_client()
