from django.contrib.auth.models import User
from django.db import models


class AudioFile(models.Model):
    audio_file_id = models.AutoField(primary_key=True)
    audio_file = models.FileField(upload_to="audio")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=5)


class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    audio_file = models.ForeignKey(
        AudioFile, on_delete=models.CASCADE, related_name="conversations"
    )


class Message(models.Model):
    SENDER_TYPES = (("user", "User"), ("assistant", "Annotated"))

    message_id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.CharField(max_length=20, choices=SENDER_TYPES)
    message = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
