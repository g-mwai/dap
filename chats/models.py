from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

class Chat(models.Model):
    sender = models.ForeignKey(User, related_name="sent_chats", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_chats", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.message}"
