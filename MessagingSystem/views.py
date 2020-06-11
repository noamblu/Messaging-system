from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from django.core import exceptions
from django.db.models import Q


class MessagesListView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.query_params.get("unread", None) == "True":
            messages = Message.objects.filter(receiver=request.user, read_status=False)
        else:
            messages = Message.objects.filter(receiver=request.user)
        messages_serializer = MessageSerializer(messages, many=True)
        return Response(messages_serializer.data)

    def post(self, request):
        data = request.data
        data['sender'] = request.user
        message_serializer = MessageSerializer(data=data)
        if message_serializer.is_valid():
            message_serializer.save()
            return Response('Message saved')
        return Response('The message is incorrect', status=status.HTTP_400_BAD_REQUEST)


class MessageDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id, receiver=request.user)
            message.read_status = True
            message.save()
            message_serializer = MessageSerializer(message)
            return Response(message_serializer.data)
        except exceptions.ObjectDoesNotExist:
            return Response("The message was not found or you must not read this message",
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, message_id):
        try:
            message = Message.objects.get(Q(id=message_id),
                                          Q(sender=request.user) | Q(receiver=request.user))
            message.delete()
            return Response("Message deleted")
        except exceptions.ObjectDoesNotExist:
            return Response("The message was not found or you must not delete this message",
                            status=status.HTTP_400_BAD_REQUEST)
