package server;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;



public class MessageBrokerServer {
    private int port;
    private Server server;



    public MessageBrokerServer(int port) {
        this.port = port;
    }



    public void start() throws IOException {
        server = ServerBuilder.forPort(port)
                .addService(new MessageBrokerServiceImpl())
                .build()
                .start();



        System.out.println("Server started on port " + port);



        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("Shutting down server...");
            MessageBrokerServer.this.stop();
            System.out.println("Server stopped");
        }));
    }



    public void stop() {
        if (server != null) {
            server.shutdown();
        }
    }



    private void blockUntilShutdown() throws InterruptedException {
        if (server != null) {
            server.awaitTermination();
        }
    }



    public static void main(String[] args) throws IOException, InterruptedException {
        MessageBrokerServer server = new MessageBrokerServer(50051);
        server.start();
        server.blockUntilShutdown();
    }



    private static class MessageBrokerServiceImpl extends MessageBrokerServiceGrpc.MessageBrokerServiceImplBase {
        @Override
        public void publishMessage(PublishMessageRequest request, StreamObserver<PublishMessageResponse> responseObserver) {
            // Lógica para publicar un mensaje en un tema
            String topic = request.getTopic();
            String message = request.getMessage();
            System.out.println("Received message: " + message + " for topic: " + topic);



            // Realizar acciones necesarias con el mensaje (almacenamiento, distribución, etc.)



            PublishMessageResponse response = PublishMessageResponse.newBuilder()
                    .setMessageId("123456") // ID del mensaje publicado
                    .build();



            responseObserver.onNext(response);
            responseObserver.onCompleted();
        }



        @Override
        public void subscribeToTopic(SubscribeToTopicRequest request, StreamObserver<SubscribeToTopicResponse> responseObserver) {
            // Lógica para suscribirse a un tema y recibir mensajes
            String topic = request.getTopic();
            System.out.println("Subscribed to topic: " + topic);



            // Realizar acciones necesarias para recibir y procesar los mensajes del tema



            SubscribeToTopicResponse response = SubscribeToTopicResponse.newBuilder()
                    .setStatus("Subscribed to topic: " + topic)
                    .build();



            responseObserver.onNext(response);
            responseObserver.onCompleted();
        }
    }
}
