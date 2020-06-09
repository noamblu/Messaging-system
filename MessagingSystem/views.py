from builtins import memoryview

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from django.core import exceptions


class MessagesView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.query_params.get("unread", None) == "True":
            messages = Message.objects.filter(receiver=request.user, read_status=False)
        else:
            messages = Message.objects.filter(receiver=request.user)
        messages_serializer = MessageSerializer(messages, many=True)
        return Response(messages_serializer.data)


class MessageView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            message = Message.objects.filter(receiver=request.user, read_status=False).latest('creation_date')
            message.read_status = True
            message.save()
            message_serializer = MessageSerializer(message)
            return Response(message_serializer.data)
        except exceptions.ObjectDoesNotExist:
            return Response("No unread messages")

    def post(self, request):
        data = request.data
        data['sender'] = request.user
        message_serializer = MessageSerializer(data=data)
        if message_serializer.is_valid():
            message_serializer.save()
            return Response('Message saved')
        return Response('The message not correct', status=status.HTTP_400_BAD_REQUEST)
