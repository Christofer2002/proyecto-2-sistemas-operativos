import os
import grpc

import message_broker_pb2
import message_broker_pb2_grpc

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def PrintTopicList(topic_list):
    print("\nLista de temas:")
    for i in range(len(topic_list)):
        print(" " + str(i + 1) + ". " + topic_list[i])


def ValidateTopic(topic_list):
    while True:
        PrintTopicList(topic_list)
        topic_index = input("\nIngrese el tema: ")
        if topic_index.isdigit() and int(topic_index) > 0 and int(topic_index) <= len(topic_list):
            topic = topic_list[int(topic_index) - 1]
            break
        else:
            print("\nTema inválido. Por favor, intente nuevamente.")
    return topic
    

def PublishMessage(stub):
    topic_list = GetTopicList(stub)
    topic = ValidateTopic(topic_list)

    message = input("Ingrese el mensaje: ")
    message_request = message_broker_pb2.MessageRequest(topic=topic, message=message)
    message_response = stub.PublishMessage(message_request)

    print(message_response.message)


def SubscribeToTopic(stub):
    topic_list = GetTopicList(stub)
    topic = ValidateTopic(topic_list)
            
    topic_request = message_broker_pb2.TopicRequest(topic=topic)
    message_response = stub.SubscribeToTopic(topic_request)

    print(message_response.message)


def ListenForNewMessages(stub, topic):
    '''Escucha los mensajes de un tema.
    try:
        print("\nEsperando mensajes en el tema " + topic + "...")
        print("Para salir del tema, presione Ctrl + C")

        topic_request = message_broker_pb2.TopicRequest(topic=topic)
        for message_response in stub.ListenForNewMessages(topic_request):
            print("Nuevo mensaje recibido:")
            print(message_response.message)

    except KeyboardInterrupt:
        print("\nSaliendo del tema " + topic + "...")
    '''



def GetTopicList(stub):
    topic_list_request = message_broker_pb2.TopicListRequest()
    topic_list_response = stub.GetTopicList(topic_list_request)
    topic_list = list(topic_list_response.topics)
    return topic_list


def GetSubscribedTopicList(stub):
    topic_list_request = message_broker_pb2.TopicListRequest()
    topic_list_response = stub.GetSubscribedTopicList(topic_list_request)
    topic_list = list(topic_list_response.topics)
    return topic_list


def run_client():
    channel = grpc.insecure_channel('localhost:50051')
    stub = message_broker_pb2_grpc.MessageBrokerServiceStub(channel)

    while True:
        print("\nMenú:")
        print(" 1. Publicar un mensaje en un tema")
        print(" 2. Suscribirse a un tema")
        print(" 3. Obtener lista de temas suscritos")
        print(" 4. Recibir mensajes de un tema")
        print(" 5. Salir")
        choice = input("\nIngrese su elección: ")

        if choice == "1":
            PublishMessage(stub)
        elif choice == "2":
            SubscribeToTopic(stub)
        elif choice == "3":
            PrintTopicList(GetSubscribedTopicList(stub))
        elif choice == "4":
            topic_list = GetSubscribedTopicList(stub)
            if len(topic_list) == 0:
                print("\nNo se encuentra suscrito a ningún tema.")
            else:
                ListenForNewMessages(stub, ValidateTopic(topic_list))
        elif choice == "5":
            break
        else:
            print("\nOpción inválida. Por favor, intente nuevamente.")


if __name__ == '__main__':
    run_client()
