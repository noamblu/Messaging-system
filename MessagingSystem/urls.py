from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
# router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path(r'', include(router.urls)),

    path('messages/', MessagesView.as_view(), name="messages"),
    path('message/', MessageView.as_view(), name="message"),
]