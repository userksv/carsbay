# chat/consumers.py
import json
from main.models import PostImage
from .models import Conversation, Message
from main.models import Post
from chat.api.serializers import MessageSerializer, ConversationSerializer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None
        self.post_id = None

    def create_message(self, conversation, user, receiver, msg):
        message, created = Message.objects.get_or_create(
                    conversation=conversation,
                    from_user = user,
                    to_user = receiver,
                    content = msg
                    )
        return message

    def get_post(self, post_id):
        return Post.objects.get(id=post_id)

    def get_conversations(self, user):
        result = []
        # Here I have a bug, problem is that if there two users with names like 'mike' and 'mike1123'
        # query will return for both users same result
        # This is temporary solution, maybe I need to implement it in model???
        # Rigth now it works)
        conversations = Conversation.objects.filter(name__iexact=user)
        # for conversation in conversations:
        #     names = conversation.name.split('__')
        #     if user.username in names:
        #         result.append(conversation)
        
        conversations = ConversationSerializer(result, many=True).data
        for i, conv in enumerate(conversations):
            # Get messages with read property False 
            count = Message.objects.filter(to_user=self.scope['user'], read=False, conversation=conv[('id')]).count()
            # Get post image from s3 bucket
            image = str(PostImage.objects.filter(post=int(conv['post']['id'])).first().get_s3_image_link())
            # messages = self.get_messages(conv[('name')])
            # Add count and image to serialized conversations 
            conversations[i].update({'unread_count': count, 'image': image})
        return conversations

    def get_current_conversation(self, name):
        try:
            return Conversation.objects.get(name=name)
        except:
            return None
    
    def get_receiver(self):
        usernames = self.conversation_name.split("__")
        for username in usernames:
            if username != self.user.username:
                # This is the receiver
                return User.objects.get(username=username)
            
    def get_messages(self, conversation_name):
        """
        Get all messages for particular conversation
        """
        conversation = self.get_current_conversation(conversation_name)
        messages = MessageSerializer(conversation.messages.all(), many=True).data
        return messages
        
    def check_conversations(self):
        """
        Delete conversation if there no messages
        """
        conversations = Conversation.objects.all()
        for conversation in conversations:
            if Message.objects.filter(conversation=conversation).count() == 0:
                conversation.delete()

    def connect(self):
        print("Connected!")
        self.user = self.scope['user']
        if self.user.is_anonymous:
            self.close()
            return
        self.accept()
        # Get unread messages count for user
        messages = Message.objects.filter(to_user=self.user, read=False)
        unread_count = messages.count()
        
        self.check_conversations()
        # Send to websocket unread_count
        self.send(json.dumps({
            'type': 'new_message_notification',
            'unread_count': unread_count,
            }))
    
    def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data['type']

        if msg_type == 'create_conversation':
            # post_id needs for grabbing post author creator
            self.post_id = data['postId']
            post = self.get_post(self.post_id)
            post_author = post.author
            self.conversation_name = f'{self.user}__{post_author}__{post.id}'
            # Create new conversation
            self.conversation, created = Conversation.objects.get_or_create(name=self.conversation_name, post=post)
            conversations = self.get_conversations(self.scope['user'])
           
            self.send(json.dumps({
                'type': 'get_conversations', 
                'conversations': conversations,
            }))
                
        if msg_type == 'get_conversations':
            # Getting all conversations for current user
            conversations = self.get_conversations(self.scope['user'])
            # print(conversations)
            self.send(json.dumps({
                'type': 'get_conversations',
                'conversations': conversations,
            }))
           
        if msg_type == 'fetch_messages':
            # Fetching messages for current conversation
            self.conversation_name = data['conversation_name']
            self.conversation = self.get_current_conversation(self.conversation_name)
     
            messages = self.get_messages(self.conversation_name)
            # Reset unread_count for current conversation
            messages_to_me = self.conversation.messages.filter(to_user=self.user)
            messages_to_me.update(read=True)
            
            # Update the unread message count
            Message.objects.filter(to_user=self.user, read=False).count()

            async_to_sync(self.channel_layer.group_add)(
            self.conversation_name, self.channel_name
            )
            self.send(json.dumps({
                'type': 'fetch_messages',
                'message': messages,
            }))
            

        if msg_type == 'chat_message':
            msg = data['message']
            # Getting current conversation object in order to pass to Message model
            self.conversation = self.get_current_conversation(self.conversation_name)
            message = self.create_message(self.conversation, self.user, self.get_receiver(), msg)
            message = MessageSerializer(message).data
            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "chat_message",
                    "name": self.user.username,
                    "message": message
                },
            )

    def new_message_notification(self, event):
        self.send(json.dumps(event))

    # Receive message from room group
    def chat_message(self, event):
        context={
            'type': event['type'],
            'username': event["name"],
            'message': event["message"],
        }
        # Send message to WebSocket
        self.send(text_data=json.dumps(context))

    def disconnect(self, close_code):
        # Leave room group
        print(close_code)
