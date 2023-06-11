# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import message_broker_pb2 as message__broker__pb2


class MessageBrokerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PublishMessage = channel.unary_unary(
                '/messagebroker.MessageBrokerService/PublishMessage',
                request_serializer=message__broker__pb2.MessageRequest.SerializeToString,
                response_deserializer=message__broker__pb2.MessageResponse.FromString,
                )
        self.SubscribeToTopic = channel.unary_unary(
                '/messagebroker.MessageBrokerService/SubscribeToTopic',
                request_serializer=message__broker__pb2.TopicRequest.SerializeToString,
                response_deserializer=message__broker__pb2.MessageResponse.FromString,
                )
        self.CheckNewMessages = channel.unary_unary(
                '/messagebroker.MessageBrokerService/CheckNewMessages',
                request_serializer=message__broker__pb2.CheckRequest.SerializeToString,
                response_deserializer=message__broker__pb2.CheckResponse.FromString,
                )
        self.GetTopicList = channel.unary_unary(
                '/messagebroker.MessageBrokerService/GetTopicList',
                request_serializer=message__broker__pb2.TopicListRequest.SerializeToString,
                response_deserializer=message__broker__pb2.TopicListResponse.FromString,
                )
        self.GetSubscribedTopicList = channel.unary_unary(
                '/messagebroker.MessageBrokerService/GetSubscribedTopicList',
                request_serializer=message__broker__pb2.TopicListRequest.SerializeToString,
                response_deserializer=message__broker__pb2.TopicListResponse.FromString,
                )
        self.ListenForNewMessages = channel.unary_stream(
                '/messagebroker.MessageBrokerService/ListenForNewMessages',
                request_serializer=message__broker__pb2.TopicRequest.SerializeToString,
                response_deserializer=message__broker__pb2.MessageResponse.FromString,
                )


class MessageBrokerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PublishMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeToTopic(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckNewMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTopicList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSubscribedTopicList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListenForNewMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MessageBrokerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PublishMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.PublishMessage,
                    request_deserializer=message__broker__pb2.MessageRequest.FromString,
                    response_serializer=message__broker__pb2.MessageResponse.SerializeToString,
            ),
            'SubscribeToTopic': grpc.unary_unary_rpc_method_handler(
                    servicer.SubscribeToTopic,
                    request_deserializer=message__broker__pb2.TopicRequest.FromString,
                    response_serializer=message__broker__pb2.MessageResponse.SerializeToString,
            ),
            'CheckNewMessages': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckNewMessages,
                    request_deserializer=message__broker__pb2.CheckRequest.FromString,
                    response_serializer=message__broker__pb2.CheckResponse.SerializeToString,
            ),
            'GetTopicList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTopicList,
                    request_deserializer=message__broker__pb2.TopicListRequest.FromString,
                    response_serializer=message__broker__pb2.TopicListResponse.SerializeToString,
            ),
            'GetSubscribedTopicList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSubscribedTopicList,
                    request_deserializer=message__broker__pb2.TopicListRequest.FromString,
                    response_serializer=message__broker__pb2.TopicListResponse.SerializeToString,
            ),
            'ListenForNewMessages': grpc.unary_stream_rpc_method_handler(
                    servicer.ListenForNewMessages,
                    request_deserializer=message__broker__pb2.TopicRequest.FromString,
                    response_serializer=message__broker__pb2.MessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messagebroker.MessageBrokerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MessageBrokerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PublishMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messagebroker.MessageBrokerService/PublishMessage',
            message__broker__pb2.MessageRequest.SerializeToString,
            message__broker__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubscribeToTopic(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messagebroker.MessageBrokerService/SubscribeToTopic',
            message__broker__pb2.TopicRequest.SerializeToString,
            message__broker__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckNewMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messagebroker.MessageBrokerService/CheckNewMessages',
            message__broker__pb2.CheckRequest.SerializeToString,
            message__broker__pb2.CheckResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTopicList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messagebroker.MessageBrokerService/GetTopicList',
            message__broker__pb2.TopicListRequest.SerializeToString,
            message__broker__pb2.TopicListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSubscribedTopicList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messagebroker.MessageBrokerService/GetSubscribedTopicList',
            message__broker__pb2.TopicListRequest.SerializeToString,
            message__broker__pb2.TopicListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListenForNewMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/messagebroker.MessageBrokerService/ListenForNewMessages',
            message__broker__pb2.TopicRequest.SerializeToString,
            message__broker__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
