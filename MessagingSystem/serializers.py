from rest_framework import serializers
from .models import *


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'message', 'subject', 'creation_date']
