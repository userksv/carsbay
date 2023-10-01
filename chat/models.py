from django.contrib.auth import get_user_model
from main.models import Post
from django.db import models
import uuid
from django.urls import reverse

User = get_user_model()

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, related_name='conversations', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ordering = ["-timestamp"]
    # How can I use this field???
    # participants = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_online_count()})"
    
    def get_absolute_url(self):
        return self.name


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages", null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_from_me")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_to_me")
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.from_user.username} to {self.to_user.username}: {self.content} [{self.timestamp}][{self.conversation.id}]"
    
    def get_conversation(self):
        return self.conversation.id
    
    def get_conversation_name(self):
        return f'{self.conversation.name}'