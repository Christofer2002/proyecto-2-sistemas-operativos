package cliente;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.stub.StreamObserver;

public class MessageBrokerClient {
    private String host;
    private int port;
    private ManagedChannel channel;
    private MessageBrokerServiceGrpc.MessageBrokerServiceStub asyncStub;

    public MessageBrokerClient(String host, int port) {
        this.host = host;
        this.port = port;
    }

    public void start() {
        channel = ManagedChannelBuilder.forAddress(host, port)
                .usePlaintext()
                .build();

        asyncStub = MessageBrokerServiceGrpc.newStub(channel);
    }

    public void stop() {
        if (channel != null) {
            channel.shutdown();
        }
    }

    public void publishMessage(String topic, String message) {
        PublishMessageRequest request = PublishMessageRequest.newBuilder()
                .setTopic(topic)
                .setMessage(message)
                .build();

        asyncStub.publishMessage(request, new StreamObserver<PublishMessageResponse>() {
            @Override
            public void onNext(PublishMessageResponse response) {
                // Lógica para manejar la respuesta del servidor al publicar un mensaje
                String messageId = response.getMessageId();
                System.out.println("Message published. Message ID: " + messageId);
            }

            @Override
            public void onError(Throwable t) {
                // Lógica para manejar errores al publicar un mensaje
                System.err.println("Error publishing message: " + t.getMessage());
            }

            @Override
            public void onCompleted() {
                // Lógica para finalizar la publicación del mensaje
                System.out.println("Message publishing completed");
            }
        });
    }

    public void subscribeToTopic(String topic) {
        SubscribeToTopicRequest request = SubscribeToTopicRequest.newBuilder()
                .setTopic(topic)
                .build();

        asyncStub.subscribeToTopic(request, new StreamObserver<SubscribeToTopicResponse>() {
            @Override
            public void onNext(SubscribeToTopicResponse response) {
                // Lógica para manejar la respuesta del servidor al suscribirse a un tema
                String status = response.getStatus();
                System.out.println("Subscription status: " + status);
            }

            @Override
            public void onError(Throwable t) {
                // Lógica para manejar errores al suscribirse a un tema
                System.err.println("Error subscribing to topic: " + t.getMessage());
            }

            @Override
            public void onCompleted() {
                // Lógica para finalizar la suscripción al tema
                System.out.println("Subscription completed");
            }
        });
    }

    public static void main(String[] args) {
        MessageBrokerClient client = new MessageBrokerClient("localhost", 50051);
        client.start();

        // Ejemplo de uso: publicar un mensaje y suscribirse a un tema
        client.publishMessage("Topic1", "Hello, Topic1!");
        client.subscribeToTopic("Topic1");

        // Esperar un tiempo para recibir mensajes antes de detener el cliente
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        client.stop();
    }
}
