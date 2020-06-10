# Messaging-system

First need to signin with exsist user

Post new message use POST request /messages/
with body 
{
        "receiver": "username",
        "message": "message body",
        "subject": "message subject",
}

Read all messages use GET request /messages/
Read all unread messages use GET request /messages/?unred=True
Read current message use GET request /messages/:id
Delete current message use DELETE request /messages/:id
