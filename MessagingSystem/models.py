from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender_user", to_field="username", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver_user", to_field="username",  on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    subject = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)
